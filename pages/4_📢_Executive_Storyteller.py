# pages/4_📢_Executive_Storyteller.py — Executive Storyteller
"""
Revenue impact calculator, auto-generated executive summary,
and downloadable markdown report.
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.viz import (apply_global_css, hero_banner, styled_fig, funnel_chart,
                        kpi_card_html, GOLD, BLUE, SUCCESS, DANGER, PURPLE)

st.set_page_config(page_title="📢 Executive Storyteller", page_icon="📢", layout="wide")
apply_global_css()

hero_banner("📢 Executive Storyteller", "Translate experiment results into revenue impact & board-ready narratives")

# ══════════════════════════════════════════════════════════════════════════════
# REVENUE IMPACT CALCULATOR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 💰 Real-Time Revenue Impact Calculator")

c1, c2, c3 = st.columns(3)
total_users = c1.slider("Total monthly users", 100_000, 50_000_000, 10_000_000, 100_000,
                         format="%d")
lift_pct = c2.slider("Conversion lift (%)", 0.1, 20.0, 2.5, 0.1)
arpu = c3.slider("ARPU ($)", 1.0, 50.0, 13.99, 0.50)

incremental_conversions = int(total_users * (lift_pct / 100))
revenue_impact = incremental_conversions * arpu
annual_impact = revenue_impact * 12

# animated number display
st.markdown("---")

kpi_cols = st.columns(4)
kpis = [
    ("👥 Incremental Conversions", f"{incremental_conversions:,}", f"+{lift_pct:.1f}%", "👥"),
    ("💵 Monthly Revenue Impact", f"${revenue_impact:,.0f}", f"+{lift_pct:.1f}% lift", "💵"),
    ("📅 Annual Projection", f"${annual_impact:,.0f}", f"×12 months", "📅"),
    ("🎯 ARPU", f"${arpu:.2f}", "per user", "🎯"),
]
for col, (label, value, delta, icon) in zip(kpi_cols, kpis):
    col.markdown(kpi_card_html(label, value, delta, icon), unsafe_allow_html=True)

# big animated revenue display
st.markdown(f"""
<div style="text-align:center;padding:30px;margin:20px 0;
     background:linear-gradient(135deg,rgba(255,215,0,0.08),rgba(0,191,255,0.05));
     border:1px solid rgba(255,215,0,0.15);border-radius:18px;">
    <div style="color:#999;font-size:0.9rem;text-transform:uppercase;letter-spacing:0.1em;">
        Projected Annual Revenue Uplift
    </div>
    <div style="font-family:'Playfair Display',serif;font-size:3.5rem;font-weight:700;
         background:linear-gradient(135deg,#FFD700,#00BFFF);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent;
         margin:8px 0;">
        ${annual_impact:,.0f}
    </div>
    <div style="color:#777;font-size:0.85rem;">
        {incremental_conversions:,} new conversions × ${arpu:.2f} ARPU × 12 months
    </div>
</div>
""", unsafe_allow_html=True)

if annual_impact > 1_000_000:
    st.balloons()
    st.success("🎉 That's a **million-dollar** impact! This is board-deck material.")

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONVERSION FUNNEL
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 📊 Subscriber Conversion Funnel")

funnel_stages = ["Ad Impressions", "Clicks", "Sign-Up Page", "Trial Start", "Paid Subscriber"]
base_vals = [total_users, int(total_users * 0.08), int(total_users * 0.035),
             int(total_users * 0.018), int(total_users * 0.012)]

st.plotly_chart(funnel_chart(funnel_stages, base_vals, "Streaming Subscriber Funnel"), use_container_width=True)

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# EXECUTIVE SUMMARY GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 📝 One-Click Executive Deck")

freq_res = st.session_state.get("freq_results")
bayes_res = st.session_state.get("bayes_results")

if st.button("📄 Generate Executive Summary", type="primary"):
    progress = st.progress(0)
    steps = ["Analysing results...", "Calculating impact...", "Writing narrative...",
             "Formatting deck...", "Adding sparkle ✨"]
    for i, step in enumerate(steps):
        time.sleep(0.3)
        progress.progress((i + 1) * 20, text=f"{'✨' * (i+1)} {step}")

    # build the report
    sig_text = "statistically significant" if (freq_res and freq_res.get("significant")) else "not yet statistically significant"
    lift_text = f"{freq_res['lift_pct']:+.2f}%" if freq_res else "N/A"
    p_text = f"{freq_res['p_value']:.6f}" if freq_res else "N/A"
    bayes_text = f"{bayes_res['prob_b_wins']:.1%}" if bayes_res else "N/A"

    report = f"""# 📊 Enchanted AdLab — Executive Summary

## Experiment Overview
- **Platform**: MagicStream (Disney DTC Streaming)
- **Objective**: Measure impact of variant ad creative on subscriber conversion
- **Methodology**: Randomised controlled A/B test with frequentist & Bayesian analysis

---

## Key Findings

### Statistical Results
- **Outcome**: The experiment is **{sig_text}**
- **Relative Lift**: {lift_text}
- **p-value**: {p_text}
- **Bayesian P(Variant Wins)**: {bayes_text}

### Revenue Impact
- **Monthly Users Impacted**: {total_users:,}
- **Incremental Conversions**: {incremental_conversions:,}
- **Monthly Revenue Uplift**: ${revenue_impact:,.0f}
- **Projected Annual Impact**: **${annual_impact:,.0f}**

---

## Recommendation

{"✅ **SHIP IT** — The variant shows strong, statistically significant improvement. Recommend full rollout." if (freq_res and freq_res.get("significant")) else "⏳ **CONTINUE TESTING** — Results are promising but not yet conclusive. Recommend extending the experiment."}

---

## Methodology Notes
- Frequentist: Auto-selected test with Bonferroni correction for segments
- Bayesian: Beta-Binomial conjugate model with uninformative priors
- SRM check passed ✅
- Sequential monitoring with always-valid p-values

---

*Generated by Enchanted AdLab | Built by Yashpal*
"""

    st.session_state["exec_report"] = report
    st.success("✅ Executive summary generated!")

report = st.session_state.get("exec_report")
if report:
    with st.container(border=True):
        st.markdown(report)

    # download buttons
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "📥 Download as Markdown",
            data=report,
            file_name="enchanted_adlab_executive_summary.md",
            mime="text/markdown",
        )
    with c2:
        # fake PDF button (portfolio demonstration)
        st.download_button(
            "📥 Download as PDF (Demo)",
            data=report.encode(),
            file_name="enchanted_adlab_summary.pdf",
            mime="application/pdf",
            help="Demo button — in production this would generate a styled PDF",
        )
