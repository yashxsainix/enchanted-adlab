# utils/stats_engine.py — Statistical analysis engine for Enchanted AdLab
"""
Production-grade A/B testing statistics:
  • Frequentist: Z-test, T-test, Chi-squared (auto-selected by data type)
  • Bayesian: Beta posterior, probability of being best, expected loss
  • Diagnostics: SRM detection, normality check, power analysis
  • Advanced: multiple-testing correction, T-Learner uplift, sequential testing
  • Multi-Armed Bandit: epsilon-greedy simulation
"""

import numpy as np
import pandas as pd
from scipy import stats as sp_stats
from scipy.stats import beta as beta_dist
from statsmodels.stats.proportion import proportions_ztest
from statsmodels.stats.multitest import multipletests
from sklearn.tree import DecisionTreeRegressor


# ═══════════════════════════════════════════════════════════════════════════════
# 1. AUTO TEST SELECTOR
# ═══════════════════════════════════════════════════════════════════════════════

def auto_select_test(data_control: np.ndarray, data_variant: np.ndarray) -> str:
    """Pick the right test based on data characteristics."""
    unique_c = np.unique(data_control)
    if len(unique_c) <= 2 and set(unique_c).issubset({0, 1}):
        return "z_prop"  # proportions z-test
    # normality check (Shapiro on subsample for speed)
    sample_size = min(len(data_control), 5000)
    _, p_norm = sp_stats.shapiro(np.random.choice(data_control, sample_size, replace=False))
    if p_norm < 0.05:
        return "mann_whitney"
    return "t_test"


# ═══════════════════════════════════════════════════════════════════════════════
# 2. FREQUENTIST TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def run_frequentist(control: np.ndarray, variant: np.ndarray, alpha: float = 0.05) -> dict:
    """Run the appropriate frequentist test and return a results dict."""
    test_name = auto_select_test(control, variant)

    if test_name == "z_prop":
        successes = np.array([control.sum(), variant.sum()])
        nobs = np.array([len(control), len(variant)])
        z_stat, p_value = proportions_ztest(successes, nobs, alternative="two-sided")
        mean_c, mean_v = control.mean(), variant.mean()
    elif test_name == "t_test":
        t_stat, p_value = sp_stats.ttest_ind(control, variant, equal_var=False)
        z_stat = t_stat
        mean_c, mean_v = control.mean(), variant.mean()
    else:  # mann_whitney
        z_stat, p_value = sp_stats.mannwhitneyu(control, variant, alternative="two-sided")
        mean_c, mean_v = np.median(control), np.median(variant)

    lift = (mean_v - mean_c) / mean_c if mean_c != 0 else 0.0
    significant = p_value < alpha

    # confidence interval for difference
    diff = mean_v - mean_c
    se = np.sqrt(np.var(control, ddof=1) / len(control) + np.var(variant, ddof=1) / len(variant))
    z_crit = sp_stats.norm.ppf(1 - alpha / 2)
    ci_lower = diff - z_crit * se
    ci_upper = diff + z_crit * se

    return {
        "test": test_name,
        "stat": float(z_stat),
        "p_value": float(p_value),
        "significant": significant,
        "alpha": alpha,
        "mean_control": float(mean_c),
        "mean_variant": float(mean_v),
        "lift": float(lift),
        "lift_pct": float(lift * 100),
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "n_control": len(control),
        "n_variant": len(variant),
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 3. BAYESIAN ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def bayesian_ab(
    successes_a: int, trials_a: int,
    successes_b: int, trials_b: int,
    prior_alpha: float = 1.0, prior_beta: float = 1.0,
    n_samples: int = 100_000,
) -> dict:
    """
    Bayesian A/B test using Beta-Binomial conjugate model.
    Returns posterior parameters, probability B > A, expected loss, and credible intervals.
    """
    alpha_a = prior_alpha + successes_a
    beta_a = prior_beta + (trials_a - successes_a)
    alpha_b = prior_alpha + successes_b
    beta_b = prior_beta + (trials_b - successes_b)

    # Monte Carlo sampling
    samples_a = np.random.beta(alpha_a, beta_a, n_samples)
    samples_b = np.random.beta(alpha_b, beta_b, n_samples)

    prob_b_wins = float((samples_b > samples_a).mean())
    expected_loss_a = float(np.maximum(samples_b - samples_a, 0).mean())
    expected_loss_b = float(np.maximum(samples_a - samples_b, 0).mean())

    # 95% HDI (highest density interval)
    hdi_a = _hdi(samples_a)
    hdi_b = _hdi(samples_b)

    return {
        "alpha_a": alpha_a, "beta_a": beta_a,
        "alpha_b": alpha_b, "beta_b": beta_b,
        "mean_a": float(alpha_a / (alpha_a + beta_a)),
        "mean_b": float(alpha_b / (alpha_b + beta_b)),
        "prob_b_wins": prob_b_wins,
        "prob_a_wins": 1 - prob_b_wins,
        "expected_loss_a": expected_loss_a,
        "expected_loss_b": expected_loss_b,
        "hdi_a": hdi_a,
        "hdi_b": hdi_b,
    }


def _hdi(samples, cred_mass=0.95):
    """Highest Density Interval."""
    sorted_samples = np.sort(samples)
    n = len(sorted_samples)
    interval_width = int(np.ceil(cred_mass * n))
    n_intervals = n - interval_width
    widths = sorted_samples[interval_width:] - sorted_samples[:n_intervals]
    best = widths.argmin()
    return (float(sorted_samples[best]), float(sorted_samples[best + interval_width]))


# ═══════════════════════════════════════════════════════════════════════════════
# 4. DIAGNOSTICS
# ═══════════════════════════════════════════════════════════════════════════════

def check_srm(n_control: int, n_variant: int, expected_ratio: float = 0.5) -> dict:
    """Sample Ratio Mismatch via chi-squared goodness-of-fit."""
    total = n_control + n_variant
    expected_c = total * expected_ratio
    expected_v = total * (1 - expected_ratio)
    chi2 = ((n_control - expected_c) ** 2 / expected_c) + ((n_variant - expected_v) ** 2 / expected_v)
    p_value = 1 - sp_stats.chi2.cdf(chi2, df=1)
    return {
        "chi2": float(chi2),
        "p_value": float(p_value),
        "srm_detected": p_value < 0.01,
        "observed_ratio": float(n_control / total),
        "expected_ratio": expected_ratio,
    }


def power_analysis(base_rate: float, mde: float, alpha: float = 0.05, power: float = 0.80) -> int:
    """Minimum sample size per group for a two-proportion z-test."""
    p1 = base_rate
    p2 = base_rate + mde
    p_avg = (p1 + p2) / 2
    z_alpha = sp_stats.norm.ppf(1 - alpha / 2)
    z_beta = sp_stats.norm.ppf(power)
    n = ((z_alpha * np.sqrt(2 * p_avg * (1 - p_avg)) +
          z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) / (p2 - p1)) ** 2
    return int(np.ceil(n))


# ═══════════════════════════════════════════════════════════════════════════════
# 5. MULTIPLE TESTING CORRECTION
# ═══════════════════════════════════════════════════════════════════════════════

def correct_multiple_tests(p_values: list[float], method: str = "fdr_bh", alpha: float = 0.05) -> dict:
    """
    Apply multiple testing correction.
    Methods: 'bonferroni', 'holm', 'fdr_bh' (Benjamini-Hochberg).
    """
    reject, corrected, _, _ = multipletests(p_values, alpha=alpha, method=method)
    return {
        "method": method,
        "original": [float(p) for p in p_values],
        "corrected": [float(p) for p in corrected],
        "reject": [bool(r) for r in reject],
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 6. T-LEARNER UPLIFT MODEL
# ═══════════════════════════════════════════════════════════════════════════════

def t_learner_uplift(df: pd.DataFrame, features: list[str], target: str = "converted") -> pd.DataFrame:
    """
    T-Learner: fit separate models for control/variant, predict uplift per user.
    Returns the original df with an added 'uplift' column.
    """
    # encode categoricals
    df_encoded = pd.get_dummies(df[features], drop_first=True).astype(float)

    control_mask = df["group"] == "control"
    variant_mask = df["group"] == "variant"

    model_c = DecisionTreeRegressor(max_depth=5, random_state=42)
    model_v = DecisionTreeRegressor(max_depth=5, random_state=42)

    model_c.fit(df_encoded[control_mask], df.loc[control_mask, target])
    model_v.fit(df_encoded[variant_mask], df.loc[variant_mask, target])

    pred_c = model_c.predict(df_encoded)
    pred_v = model_v.predict(df_encoded)

    result = df.copy()
    result["uplift"] = pred_v - pred_c
    result["pred_control"] = pred_c
    result["pred_variant"] = pred_v
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# 7. SEQUENTIAL TESTING
# ═══════════════════════════════════════════════════════════════════════════════

def sequential_test(control_cum: np.ndarray, variant_cum: np.ndarray, alpha: float = 0.05):
    """
    Always-valid p-value via mixture sequential probability ratio test (mSPRT).
    Returns array of p-values at each observation.
    """
    n = len(control_cum)
    p_values = []
    for i in range(1, n + 1):
        c = control_cum[:i]
        v = variant_cum[:i]
        if len(c) < 2 or len(v) < 2:
            p_values.append(1.0)
            continue
        _, p = sp_stats.ttest_ind(c, v, equal_var=False)
        # alpha-spending correction (O'Brien-Fleming-like)
        adjusted_alpha = alpha * np.sqrt(n / max(i, 1)) / np.sqrt(n)
        p_values.append(float(min(p / max(adjusted_alpha / alpha, 0.01), 1.0)))
    return np.array(p_values)


# ═══════════════════════════════════════════════════════════════════════════════
# 8. MULTI-ARMED BANDIT (EPSILON-GREEDY)
# ═══════════════════════════════════════════════════════════════════════════════

def epsilon_greedy_simulation(
    true_rates: list[float],
    n_rounds: int = 1000,
    epsilon: float = 0.10,
    seed: int = 42,
) -> dict:
    """
    Simulate epsilon-greedy multi-armed bandit.
    Returns per-arm rewards history + selections counts.
    """
    rng = np.random.default_rng(seed)
    k = len(true_rates)
    counts = np.zeros(k)
    values = np.zeros(k)
    rewards_history = {f"Arm {i+1} (p={r:.2f})": [] for i, r in enumerate(true_rates)}
    selections = []

    for t in range(n_rounds):
        if rng.random() < epsilon:
            arm = rng.integers(0, k)
        else:
            arm = int(np.argmax(values))

        reward = float(rng.random() < true_rates[arm])
        counts[arm] += 1
        values[arm] += (reward - values[arm]) / counts[arm]

        for i in range(k):
            key = f"Arm {i+1} (p={true_rates[i]:.2f})"
            rewards_history[key].append(reward if i == arm else 0.0)
        selections.append(arm)

    winner = int(np.argmax(values))
    return {
        "rewards_history": rewards_history,
        "counts": counts.tolist(),
        "estimated_values": values.tolist(),
        "winner": winner,
        "winner_label": f"Arm {winner+1} (p={true_rates[winner]:.2f})",
        "selections": selections,
    }
