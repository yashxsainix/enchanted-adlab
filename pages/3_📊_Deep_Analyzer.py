# pages/3_📊_Deep_Analyzer.py — Deep Analyzer
"""
Advanced analysis: segment-level treatment effects, T-Learner uplift modelling,
multiple testing correction, and Multi-Armed Bandit arena.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.viz import (apply_global_css, hero_banner, styled_fig, bandit_chart,
                        waterfall_chart, GOLD, BLUE, SUCCESS, DANGER, PURPLE)
from utils.stats_engine import (run_frequentist, correct_multiple_tests,
                                 t_learner_uplift, epsilon_greedy_simulation)
from utils.data_generator import generate_ab_data

st.set_page_config(page_title="📊 Deep Analyzer", page_icon="📊", layout="wide")
apply_global_css()

hero_banner("📊 Deep Analyzer", "Segment uplift, multi-armed bandits, and multiple testing correction")

# ══════════════════════════════════════════════════════════════════════════════
# DATA CHECK
# ══════════════════════════════════════════════════════════════════════════════
df = st.session_state.get("experiment_data")
if df is None:
    st.warning("⚠️ No experiment data found. Go to **🔬 Experiment Simulator** and generate data first.")
    if st.button("Generate quick demo data"):
        df = generate_ab_data(5000, 5000, 0.12, 0.02, "beta", 42)
        st.session_state["experiment_data"] = df
        st.rerun()
    st.stop()

tab_seg, tab_uplift, tab_multi, tab_bandit = st.tabs([
    "📊 Segment Analysis", "🎯 T-Learner Uplift", "🔧 Multiple Testing", "🎰 Bandit Arena"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — SEGMENT ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab_seg:
    st.markdown("#### Heterogeneous Treatment Effects by Segment")
    segment_col = st.selectbox("Segment dimension", ["device", "age_group", "genre", "region", "plan"])

    segments = df[segment_col].unique()
    results = []
    for seg in segments:
        seg_df = df[df[segment_col] == seg]
        c = seg_df[seg_df["group"] == "control"]["metric"].values
        v = seg_df[seg_df["group"] == "variant"]["metric"].values
        if len(c) > 10 and len(v) > 10:
            res = run_frequentist(c, v, 0.05)
            res["segment"] = seg
            res["n"] = len(seg_df)
            results.append(res)

    if results:
        res_df = pd.DataFrame(results)

        # heatmap: lift by segment
        fig_heat = go.Figure(go.Bar(
            x=res_df["segment"], y=res_df["lift_pct"],
            marker_color=[SUCCESS if p < 0.05 else "#555" for p in res_df["p_value"]],
            text=[f"{l:+.2f}%<br>p={p:.3f}" for l, p in zip(res_df["lift_pct"], res_df["p_value"])],
            textposition="outside",
        ))
        fig_heat.update_layout(
            title=f"Lift by {segment_col.replace('_',' ').title()}",
            xaxis_title=segment_col, yaxis_title="Relative Lift (%)",
        )
        st.plotly_chart(styled_fig(fig_heat), use_container_width=True)

        # waterfall
        st.plotly_chart(
            waterfall_chart(res_df["segment"].tolist(), res_df["lift_pct"].tolist(),
                            f"Segment Uplift Waterfall — {segment_col}"),
            use_container_width=True,
        )

        with st.expander("🤓 Nerd Mode — Segment-Level Results Table"):
            st.dataframe(res_df[["segment", "n", "mean_control", "mean_variant",
                                  "lift_pct", "p_value", "significant"]],
                         use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — T-LEARNER UPLIFT
# ══════════════════════════════════════════════════════════════════════════════
with tab_uplift:
    st.markdown("#### 🎯 T-Learner Uplift Modelling")
    st.caption("Fit separate models on control and variant to estimate individual-level uplift (CATE).")

    features = ["genre", "device", "age_group", "region", "plan"]
    if st.button("Train T-Learner Model", key="train_tlearner"):
        with st.spinner("Training separate control & variant models..."):
            uplift_df = t_learner_uplift(df, features, "converted")
            st.session_state["uplift_df"] = uplift_df
        st.success("✅ T-Learner trained!")

    uplift_df = st.session_state.get("uplift_df")
    if uplift_df is not None:
        # uplift distribution
        fig_up = go.Figure()
        fig_up.add_trace(go.Histogram(
            x=uplift_df["uplift"], nbinsx=60,
            marker_color=GOLD, opacity=0.75, name="CATE",
        ))
        fig_up.add_vline(x=0, line_dash="dash", line_color="white")
        fig_up.update_layout(title="Distribution of Individual Treatment Effects (CATE)",
                             xaxis_title="Uplift", yaxis_title="Count")
        st.plotly_chart(styled_fig(fig_up), use_container_width=True)

        # top/bottom segments
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**🏆 Top Uplift Segments**")
            top = (uplift_df.groupby("genre")["uplift"].mean()
                   .sort_values(ascending=False).head(5))
            for genre, val in top.items():
                bar_pct = min(abs(val) * 500, 100)
                colour = SUCCESS if val > 0 else DANGER
                st.markdown(f"**{genre}**: {val:+.4f}")
                st.progress(bar_pct / 100)
        with c2:
            st.markdown("**📉 Lowest Uplift Segments**")
            bot = (uplift_df.groupby("device")["uplift"].mean()
                   .sort_values().head(5))
            for dev, val in bot.items():
                st.markdown(f"**{dev}**: {val:+.4f}")
                st.progress(min(abs(val) * 500, 100) / 100)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — MULTIPLE TESTING CORRECTION
# ══════════════════════════════════════════════════════════════════════════════
with tab_multi:
    st.markdown("#### 🔧 Multiple Testing Correction")
    st.caption("When you test many segments, false positives pile up. Apply corrections.")

    method = st.selectbox("Correction method", ["bonferroni", "holm", "fdr_bh"],
                          format_func=lambda x: {"bonferroni": "Bonferroni (conservative)",
                                                  "holm": "Holm (step-down)",
                                                  "fdr_bh": "Benjamini-Hochberg FDR"}[x])

    seg_col = st.selectbox("Segment for testing", ["device", "age_group", "genre", "region"], key="multi_seg")
    p_values = []
    seg_names = []
    for seg in df[seg_col].unique():
        seg_df = df[df[seg_col] == seg]
        c = seg_df[seg_df["group"] == "control"]["metric"].values
        v = seg_df[seg_df["group"] == "variant"]["metric"].values
        if len(c) > 10 and len(v) > 10:
            res = run_frequentist(c, v)
            p_values.append(res["p_value"])
            seg_names.append(seg)

    if p_values and st.button("Apply Correction", key="apply_multi"):
        corrected = correct_multiple_tests(p_values, method)

        comp_df = pd.DataFrame({
            "Segment": seg_names,
            "Original p": corrected["original"],
            "Corrected p": corrected["corrected"],
            "Reject H₀": corrected["reject"],
        })

        # comparison chart
        fig_multi = go.Figure()
        fig_multi.add_trace(go.Bar(
            x=seg_names, y=corrected["original"],
            name="Original p-value", marker_color=BLUE, opacity=0.7,
        ))
        fig_multi.add_trace(go.Bar(
            x=seg_names, y=corrected["corrected"],
            name="Corrected p-value", marker_color=GOLD, opacity=0.9,
        ))
        fig_multi.add_hline(y=0.05, line_dash="dash", line_color=DANGER,
                            annotation_text="α = 0.05")
        fig_multi.update_layout(title=f"Multiple Testing Correction — {method}",
                                barmode="group", yaxis_title="p-value")
        st.plotly_chart(styled_fig(fig_multi), use_container_width=True)
        st.dataframe(comp_df, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — MULTI-ARMED BANDIT ARENA
# ══════════════════════════════════════════════════════════════════════════════
with tab_bandit:
    st.markdown("#### 🎰 Multi-Armed Bandit Arena")
    st.caption("Epsilon-greedy exploration vs exploitation — watch arms compete live!")

    c1, c2, c3 = st.columns(3)
    n_arms = c1.slider("Number of arms", 2, 5, 3)
    n_rounds = c2.slider("Rounds", 100, 5000, 1000, 100)
    epsilon = c3.slider("Epsilon (exploration)", 0.01, 0.50, 0.10, 0.01)

    arm_rates = []
    cols = st.columns(n_arms)
    for i in range(n_arms):
        with cols[i]:
            rate = st.slider(f"Arm {i+1} true rate", 0.01, 0.50,
                             round(0.05 + i * 0.05, 2), 0.01, key=f"arm_{i}")
            arm_rates.append(rate)

    if st.button("🏁 Run Bandit Simulation", type="primary", key="run_bandit"):
        result = epsilon_greedy_simulation(arm_rates, n_rounds, epsilon)
        st.session_state["bandit_result"] = result

    bres = st.session_state.get("bandit_result")
    if bres:
        st.plotly_chart(bandit_chart(bres["rewards_history"]), use_container_width=True)

        # winner announcement
        st.markdown(f"""
        <div style="text-align:center;padding:20px;background:rgba(255,215,0,0.06);
             border:1px solid rgba(255,215,0,0.2);border-radius:14px;margin:12px 0;">
            <div style="font-size:2.8rem;">👑</div>
            <div style="color:#FFD700;font-size:1.3rem;font-weight:700;">
                Winner: {bres['winner_label']}
            </div>
            <div style="color:#999;font-size:0.85rem;margin-top:4px;">
                Selected {int(bres['counts'][bres['winner']]):,} times out of {n_rounds:,} rounds
            </div>
        </div>
        """, unsafe_allow_html=True)

        # selection counts
        sel_cols = st.columns(len(arm_rates))
        for i, (cnt, est) in enumerate(zip(bres["counts"], bres["estimated_values"])):
            with sel_cols[i]:
                crown = " 👑" if i == bres["winner"] else ""
                st.metric(f"Arm {i+1}{crown}", f"{int(cnt):,} pulls", f"Est: {est:.4f}")

        st.balloons()
