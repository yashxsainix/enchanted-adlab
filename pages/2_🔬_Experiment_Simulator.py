# pages/2_🔬_Experiment_Simulator.py — A/B Experiment Simulator
"""
Core experiment engine: synthetic data generation, frequentist + Bayesian tests,
SRM detection, power analysis, distribution visualisation, and sequential testing.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.viz import (apply_global_css, hero_banner, styled_fig, distribution_chart,
                        bayesian_posterior_chart, kpi_card_html, GOLD, BLUE, SUCCESS, DANGER)
from utils.data_generator import generate_ab_data
from utils.stats_engine import (run_frequentist, bayesian_ab, check_srm,
                                 power_analysis, sequential_test)

st.set_page_config(page_title="🔬 Experiment Simulator", page_icon="🔬", layout="wide")
apply_global_css()

hero_banner("🔬 Experiment Simulator", "Design, run, and analyse streaming A/B experiments end-to-end")

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR CONTROLS
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ⚙️ Experiment Config")
    n_control = st.slider("Control group size", 500, 50000, 5000, 500)
    n_variant = st.slider("Variant group size", 500, 50000, 5000, 500)
    base_rate = st.slider("Base conversion rate", 0.01, 0.50, 0.12, 0.01)
    effect_size = st.slider("Absolute effect size (lift)", -0.05, 0.15, 0.02, 0.005)
    distribution = st.selectbox("Data distribution", ["beta", "normal", "poisson"])
    alpha = st.slider("Significance level (α)", 0.01, 0.10, 0.05, 0.01)
    seed = st.number_input("Random seed", 1, 9999, 42)

# ══════════════════════════════════════════════════════════════════════════════
# DATA GENERATION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🎲 Step 1 — Generate Synthetic Data")

if st.button("🚀 Generate Experiment Data", type="primary"):
    with st.spinner(""):
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.008)
            progress.progress(i + 1, text=f"{'✨' * ((i//20)+1)} Generating users... {i+1}%")

        df = generate_ab_data(n_control, n_variant, base_rate, effect_size, distribution, seed)
        st.session_state["experiment_data"] = df
        st.session_state["freq_results"] = None
        st.session_state["bayes_results"] = None
    st.success(f"✅ Generated **{len(df):,}** users ({n_control:,} control + {n_variant:,} variant)")

df = st.session_state.get("experiment_data")
if df is None:
    st.info("👆 Configure parameters in the sidebar and click **Generate** to start.")
    st.stop()

# ── data preview ──
with st.expander("🔍 Preview raw data (first 100 rows)", expanded=False):
    st.dataframe(df.head(100), use_container_width=True, height=300)

# ── quick summary metrics ──
control = df[df["group"] == "control"]
variant = df[df["group"] == "variant"]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Control CVR", f"{control['converted'].mean():.4f}")
c2.metric("Variant CVR", f"{variant['converted'].mean():.4f}")
c3.metric("Observed Lift", f"{((variant['converted'].mean() - control['converted'].mean())/max(control['converted'].mean(),1e-9))*100:.2f}%")
c4.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DISTRIBUTION VIZ
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 📊 Step 2 — Visualise Distributions")
fig_dist = distribution_chart(
    control["metric"].values, variant["metric"].values,
    title="Metric Distribution: Control vs Variant"
)
st.plotly_chart(fig_dist, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# DIAGNOSTICS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🩺 Step 3 — Pre-Flight Diagnostics")

col_srm, col_power = st.columns(2)

with col_srm:
    with st.container(border=True):
        st.markdown("#### 🔎 Sample Ratio Mismatch (SRM)")
        srm = check_srm(len(control), len(variant))
        if srm["srm_detected"]:
            st.error(f"⚠️ SRM DETECTED — observed ratio {srm['observed_ratio']:.3f} "
                     f"(expected {srm['expected_ratio']:.3f}), χ²={srm['chi2']:.2f}, p={srm['p_value']:.4f}")
        else:
            st.success(f"✅ No SRM — ratio {srm['observed_ratio']:.3f} looks healthy "
                       f"(χ²={srm['chi2']:.2f}, p={srm['p_value']:.4f})")

with col_power:
    with st.container(border=True):
        st.markdown("#### ⚡ Power Analysis")
        mde_input = st.number_input("Min Detectable Effect (MDE)", 0.001, 0.10, abs(effect_size) or 0.02, 0.001)
        target_power = st.slider("Target power", 0.70, 0.99, 0.80, 0.05, key="power_slider")
        required_n = power_analysis(base_rate, mde_input, alpha, target_power)
        st.metric("Required n per group", f"{required_n:,}")
        if n_control >= required_n:
            st.success(f"✅ Your sample ({n_control:,}) exceeds the requirement")
        else:
            st.warning(f"⚠️ Need {required_n - n_control:,} more per group")

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FREQUENTIST TAB + BAYESIAN TAB
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🧪 Step 4 — Statistical Testing")

tab_freq, tab_bayes, tab_seq = st.tabs(["📐 Frequentist", "🎯 Bayesian", "📈 Sequential"])

# ── Frequentist ──────────────────────────────────────────────────────────────
with tab_freq:
    if st.button("Run Frequentist Test", key="run_freq"):
        res = run_frequentist(control["metric"].values, variant["metric"].values, alpha)
        st.session_state["freq_results"] = res

    res = st.session_state.get("freq_results")
    if res:
        # verdict banner
        if res["significant"]:
            st.success(f"🎉 **SIGNIFICANT** — p={res['p_value']:.6f} < α={alpha} | "
                       f"Lift: **{res['lift_pct']:+.2f}%** | Test: {res['test']}")
            if res["lift_pct"] > 5:
                st.balloons()
        else:
            st.warning(f"❌ Not significant — p={res['p_value']:.4f} ≥ α={alpha} | "
                       f"Lift: {res['lift_pct']:+.2f}% | Test: {res['test']}")

        # metrics row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Test Statistic", f"{res['stat']:.4f}")
        m2.metric("p-value", f"{res['p_value']:.6f}")
        m3.metric("95% CI (Δ)", f"[{res['ci_lower']:.4f}, {res['ci_upper']:.4f}]")
        m4.metric("Relative Lift", f"{res['lift_pct']:+.2f}%")

        # CI chart
        fig_ci = go.Figure()
        fig_ci.add_trace(go.Scatter(
            x=[res["ci_lower"], res["ci_upper"]],
            y=["Difference", "Difference"],
            mode="lines+markers",
            line=dict(color=GOLD, width=4),
            marker=dict(size=12),
            name="95% CI",
        ))
        fig_ci.add_vline(x=0, line_dash="dash", line_color="rgba(255,255,255,0.3)")
        fig_ci.add_trace(go.Scatter(
            x=[res["mean_variant"] - res["mean_control"]],
            y=["Difference"],
            mode="markers",
            marker=dict(size=16, color=BLUE, symbol="diamond"),
            name="Point Estimate",
        ))
        fig_ci.update_layout(title="Confidence Interval for Treatment Effect",
                             xaxis_title="Δ (Variant − Control)", showlegend=True)
        st.plotly_chart(styled_fig(fig_ci, 280), use_container_width=True)

        with st.expander("🤓 Nerd Mode — Full Details"):
            st.json(res)

# ── Bayesian ─────────────────────────────────────────────────────────────────
with tab_bayes:
    st.markdown("#### 🎯 Bayesian Beta-Binomial Analysis")
    prior_a = st.slider("Prior α", 0.5, 10.0, 1.0, 0.5, key="prior_a")
    prior_b = st.slider("Prior β", 0.5, 10.0, 1.0, 0.5, key="prior_b")

    if st.button("Run Bayesian Analysis", key="run_bayes"):
        bres = bayesian_ab(
            int(control["converted"].sum()), len(control),
            int(variant["converted"].sum()), len(variant),
            prior_a, prior_b,
        )
        st.session_state["bayes_results"] = bres

    bres = st.session_state.get("bayes_results")
    if bres:
        # posterior chart
        fig_post = bayesian_posterior_chart(bres["alpha_a"], bres["beta_a"], bres["alpha_b"], bres["beta_b"])
        st.plotly_chart(fig_post, use_container_width=True)

        b1, b2, b3 = st.columns(3)
        b1.metric("P(Variant Wins)", f"{bres['prob_b_wins']:.1%}")
        b2.metric("Expected Loss (choose A)", f"{bres['expected_loss_a']:.5f}")
        b3.metric("Expected Loss (choose B)", f"{bres['expected_loss_b']:.5f}")

        # HDI display
        st.markdown(f"**Control 95% HDI:** [{bres['hdi_a'][0]:.4f}, {bres['hdi_a'][1]:.4f}]")
        st.markdown(f"**Variant 95% HDI:** [{bres['hdi_b'][0]:.4f}, {bres['hdi_b'][1]:.4f}]")

        if bres["prob_b_wins"] > 0.95:
            st.success("🏆 Strong evidence: Variant is the winner! Ship it! 🚀")
            st.balloons()
        elif bres["prob_b_wins"] > 0.80:
            st.info("📊 Moderate evidence favouring Variant — consider extending the test.")
        else:
            st.warning("⚖️ Inconclusive — keep testing or increase sample size.")

        with st.expander("🤓 Nerd Mode — Full Bayesian Results"):
            st.json(bres)

# ── Sequential ───────────────────────────────────────────────────────────────
with tab_seq:
    st.markdown("#### 📈 Sequential Testing (Always-Valid p-values)")
    st.caption("Monitor the experiment as data accumulates — stop early with valid inference.")

    if st.button("Run Sequential Monitor", key="run_seq"):
        c_vals = control["metric"].values
        v_vals = variant["metric"].values
        min_len = min(len(c_vals), len(v_vals))
        p_vals = sequential_test(c_vals[:min_len], v_vals[:min_len], alpha)

        fig_seq = go.Figure()
        fig_seq.add_trace(go.Scatter(
            y=p_vals, mode="lines", name="Sequential p-value",
            line=dict(color=GOLD, width=2),
        ))
        fig_seq.add_hline(y=alpha, line_dash="dash", line_color=DANGER,
                          annotation_text=f"α = {alpha}")
        fig_seq.update_layout(
            title="Sequential p-value Over Time",
            xaxis_title="Observation", yaxis_title="p-value",
            yaxis=dict(range=[0, min(1.0, p_vals.max() * 1.2)]),
        )
        st.plotly_chart(styled_fig(fig_seq), use_container_width=True)

        first_sig = np.where(p_vals < alpha)[0]
        if len(first_sig) > 0:
            st.success(f"🎯 Significance reached at observation **{first_sig[0]:,}** — "
                       f"you could have stopped {min_len - first_sig[0]:,} observations early!")
        else:
            st.info("🔄 No early stopping point found at this α level.")
