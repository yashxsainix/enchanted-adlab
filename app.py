# app.py — Enchanted AdLab: MagicStream A/B Experiment Simulator
# Main entry point with sidebar navigation, session state, and global theming.
"""
Built by Yashpal Saini to crush the Disney Associate Data Analyst role.
Run: streamlit run app.py
"""

import streamlit as st
import sys, os

# ── ensure project root is importable ──
sys.path.insert(0, os.path.dirname(__file__))

from utils.viz import apply_global_css, hero_banner, GOLD, BLUE

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG — must be the first Streamlit call
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="✨ Enchanted AdLab",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── inject global CSS + sparkle particles ──
apply_global_css()

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE DEFAULTS
# ══════════════════════════════════════════════════════════════════════════════
if "experiment_data" not in st.session_state:
    st.session_state["experiment_data"] = None
if "freq_results" not in st.session_state:
    st.session_state["freq_results"] = None
if "bayes_results" not in st.session_state:
    st.session_state["bayes_results"] = None

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — branding + navigation info
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:12px 0 8px;">
        <div style="font-size:2.2rem;">✨</div>
        <div style="font-family:'Playfair Display',serif;font-size:1.3rem;
             background:linear-gradient(135deg,#FFD700,#00BFFF);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             font-weight:700;">Enchanted AdLab</div>
        <div style="color:#777;font-size:0.75rem;margin-top:2px;">MagicStream A/B Simulator</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(255,215,0,0.06);border:1px solid rgba(255,215,0,0.15);
         border-radius:10px;padding:10px 14px;margin:8px 0;">
        <div style="color:#FFD700;font-size:0.78rem;font-weight:600;">🔥 Built by Yashpal Saini</div>
        <div style="color:#999;font-size:0.72rem;margin-top:2px;">
            Targeting: Disney Associate Data Analyst
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("📂 Navigate using the sidebar pages above")
    st.caption("💡 Each page is a standalone module")

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;color:#555;font-size:0.68rem;">
        Python • Streamlit • Plotly • SciPy<br>
        Statsmodels • Scikit-learn • DuckDB<br><br>
        ⭐ Star on GitHub if you like it!
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN PAGE — Landing / Home
# ══════════════════════════════════════════════════════════════════════════════

hero_banner(
    "✨ Enchanted AdLab",
    "MagicStream A/B Experiment Simulator — Test blockbuster streaming ads like Disney DTC"
)

# ── top banner ──
st.markdown("""
<div style="background:linear-gradient(135deg,rgba(255,215,0,0.08),rgba(0,191,255,0.06));
     border:1px solid rgba(255,215,0,0.12);border-radius:14px;padding:20px 28px;margin-bottom:24px;">
    <div style="color:#FFD700;font-size:1.1rem;font-weight:700;">
        🔥 Built by Yashpal Saini to crush Disney Associate Data Analyst role
    </div>
    <div style="color:#bbb;font-size:0.88rem;margin-top:6px;">
        An end-to-end A/B testing platform — from ad creative design to executive storytelling.<br>
        Navigate the pages in the sidebar to explore each module.
    </div>
</div>
""", unsafe_allow_html=True)

# ── feature cards ──
cols = st.columns(3)
features = [
    ("🎨", "Ad Creative Studio", "Upload & compare ad creatives with engagement prediction"),
    ("🔬", "Experiment Simulator", "Run frequentist + Bayesian A/B tests with synthetic data"),
    ("📊", "Deep Analyzer", "Segment uplift, multi-armed bandits, multiple testing correction"),
    ("📢", "Executive Storyteller", "Revenue calculator + one-click board deck generator"),
    ("🧪", "SQL Lab & Gallery", "DuckDB SQL engine with 5 pre-loaded Disney queries"),
    ("🚀", "Learn & Impress", "Skills mapping, quiz, and Easter egg"),
]

for i, (icon, title, desc) in enumerate(features):
    with cols[i % 3]:
        with st.container(border=True):
            st.markdown(f"### {icon} {title}")
            st.caption(desc)

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ── quick stats ──
st.markdown("#### 📈 Platform Stats")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Statistical Tests", "6+", "Z, T, χ², Bayesian, Sequential, Bandit")
c2.metric("Chart Types", "15+", "All Plotly — zero matplotlib")
c3.metric("SQL Queries", "5", "Pre-loaded Disney-style")
c4.metric("Lines of Code", "2,500+", "Production-grade Python")

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#555;font-size:0.8rem;'>"
    "✨ Enchanted AdLab v1.0 — Open Source under MIT License"
    "</div>",
    unsafe_allow_html=True,
)
