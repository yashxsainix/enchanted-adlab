# utils/data_generator.py — Synthetic data factory for Enchanted AdLab
"""
Generates realistic streaming/ad experiment datasets.
Supports Beta (conversion), Poisson (count), and Normal (revenue) distributions
with configurable effect sizes, segments, and time components.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# ── Segment catalogues (Disney-style) ────────────────────────────────────────
GENRES = ["Action", "Animation", "Comedy", "Drama", "Sci-Fi", "Documentary"]
DEVICES = ["Smart TV", "Mobile", "Tablet", "Desktop", "Game Console"]
AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+"]
REGIONS = ["North America", "EMEA", "APAC", "LATAM"]
PLANS = ["Basic", "Standard", "Premium"]
CREATIVES = ["Hero Banner", "Teaser Clip", "Carousel", "Interactive Overlay", "Pre-Roll 15s", "Mid-Roll 30s"]


def generate_ab_data(
    n_control: int = 5000,
    n_variant: int = 5000,
    base_rate: float = 0.12,
    effect_size: float = 0.02,
    distribution: str = "beta",
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate a full experiment DataFrame with demographics, metrics, and timestamps.

    Parameters
    ----------
    n_control : int   — users in control arm
    n_variant : int   — users in variant arm
    base_rate : float — control conversion/mean
    effect_size : float — absolute lift for variant
    distribution : str — 'beta' | 'poisson' | 'normal'
    seed : int

    Returns
    -------
    pd.DataFrame with columns: user_id, group, converted, revenue, metric,
        genre, device, age_group, region, plan, creative, timestamp
    """
    rng = np.random.default_rng(seed)
    n_total = n_control + n_variant

    # ── group assignment ──
    groups = np.array(["control"] * n_control + ["variant"] * n_variant)

    # ── primary metric generation ──
    if distribution == "beta":
        p_control = base_rate
        p_variant = base_rate + effect_size
        metric_c = rng.binomial(1, p_control, n_control).astype(float)
        metric_v = rng.binomial(1, p_variant, n_variant).astype(float)
    elif distribution == "poisson":
        lam_control = base_rate * 100  # scale for count data
        lam_variant = (base_rate + effect_size) * 100
        metric_c = rng.poisson(lam_control, n_control).astype(float)
        metric_v = rng.poisson(lam_variant, n_variant).astype(float)
    else:  # normal
        metric_c = rng.normal(base_rate * 100, 15, n_control)
        metric_v = rng.normal((base_rate + effect_size) * 100, 15, n_variant)

    metric = np.concatenate([metric_c, metric_v])
    converted = (metric > 0).astype(int) if distribution != "beta" else metric.astype(int)

    # ── revenue (log-normal, correlated with conversion) ──
    base_rev = rng.lognormal(mean=2.5, sigma=0.8, size=n_total)
    revenue = np.where(converted == 1, base_rev * (1 + rng.uniform(0.5, 2.0, n_total)), 0.0)
    revenue = np.round(revenue, 2)

    # ── segment dimensions ──
    genre = rng.choice(GENRES, n_total)
    device = rng.choice(DEVICES, n_total, p=[0.35, 0.30, 0.15, 0.12, 0.08])
    age_group = rng.choice(AGE_GROUPS, n_total)
    region = rng.choice(REGIONS, n_total, p=[0.40, 0.28, 0.22, 0.10])
    plan = rng.choice(PLANS, n_total, p=[0.30, 0.45, 0.25])
    creative = rng.choice(CREATIVES, n_total)

    # ── timestamps (last 14 days) ──
    start = datetime.now() - timedelta(days=14)
    timestamps = [start + timedelta(seconds=int(rng.uniform(0, 14 * 86400))) for _ in range(n_total)]

    df = pd.DataFrame({
        "user_id": [f"U{str(i).zfill(7)}" for i in range(n_total)],
        "group": groups,
        "converted": converted,
        "revenue": revenue,
        "metric": np.round(metric, 4),
        "genre": genre,
        "device": device,
        "age_group": age_group,
        "region": region,
        "plan": plan,
        "creative": creative,
        "timestamp": timestamps,
    })

    # shuffle so control/variant are interspersed
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


def generate_timeseries(n_days: int = 30, base_rate: float = 0.12, lift: float = 0.02, seed: int = 42):
    """Daily conversion rate timeseries for sequential testing visualisation."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=datetime.now().date(), periods=n_days, freq="D")
    control = base_rate + rng.normal(0, 0.005, n_days)
    variant = base_rate + lift + rng.normal(0, 0.005, n_days)
    return pd.DataFrame({"date": dates, "control_rate": control, "variant_rate": variant})


def generate_sample_csv(path: str = "sample_data.csv", n: int = 10000, seed: int = 42):
    """Write a sample dataset to disk for the SQL Lab."""
    df = generate_ab_data(n // 2, n // 2, seed=seed)
    df.to_csv(path, index=False)
    return path
