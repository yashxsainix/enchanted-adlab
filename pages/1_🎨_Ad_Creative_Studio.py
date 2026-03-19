# pages/1_🎨_Ad_Creative_Studio.py — Ad Creative Studio
"""
Upload or select cinematic ad creatives, tag them, compare side-by-side,
and get engagement score predictions via animated gauges.
"""

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.viz import apply_global_css, hero_banner, styled_fig, GOLD, BLUE, SUCCESS, kpi_card_html

st.set_page_config(page_title="🎨 Ad Creative Studio", page_icon="🎨", layout="wide")
apply_global_css()

hero_banner("🎨 Ad Creative Studio", "Design, upload, and compare streaming ad creatives")

# ══════════════════════════════════════════════════════════════════════════════
# PLACEHOLDER CREATIVES (colour-block SVG data URIs as safe fallback)
# ══════════════════════════════════════════════════════════════════════════════
PLACEHOLDER_CREATIVES = {
    "🦁 Savanna Epic": {"genre": "Animation", "mood": "Adventurous", "cta": "Watch Now", "color": "#D4A017"},
    "🚀 Galaxy Quest": {"genre": "Sci-Fi", "mood": "Thrilling", "cta": "Stream Free", "color": "#1A237E"},
    "🏰 Castle Dreams": {"genre": "Fantasy", "mood": "Magical", "cta": "Start Trial", "color": "#6A1B9A"},
    "🌊 Ocean Tales": {"genre": "Documentary", "mood": "Inspiring", "cta": "Dive In", "color": "#00695C"},
    "😂 Laugh Track": {"genre": "Comedy", "mood": "Fun", "cta": "LOL Now", "color": "#E65100"},
    "🎭 Midnight Drama": {"genre": "Drama", "mood": "Intense", "cta": "Experience", "color": "#B71C1C"},
}


def _placeholder_html(name, info, width=280, height=160):
    """Generate a colourful placeholder card for a creative."""
    return f"""
    <div style="width:{width}px;height:{height}px;border-radius:14px;
         background:linear-gradient(135deg,{info['color']}CC,{info['color']}88);
         display:flex;flex-direction:column;justify-content:center;align-items:center;
         border:1px solid rgba(255,255,255,0.1);box-shadow:0 6px 24px rgba(0,0,0,0.4);
         font-family:'DM Sans',sans-serif;">
        <div style="font-size:2.4rem;">{name.split()[0]}</div>
        <div style="color:#fff;font-weight:700;font-size:1rem;margin-top:4px;">{name}</div>
        <div style="color:rgba(255,255,255,0.7);font-size:0.75rem;margin-top:2px;">{info['genre']} · {info['mood']}</div>
        <div style="margin-top:10px;background:rgba(255,255,255,0.2);padding:4px 16px;
             border-radius:20px;font-size:0.75rem;color:#fff;font-weight:600;">{info['cta']}</div>
    </div>"""


# ══════════════════════════════════════════════════════════════════════════════
# UPLOAD OR SELECT
# ══════════════════════════════════════════════════════════════════════════════
tab_upload, tab_gallery = st.tabs(["📤 Upload Your Creative", "🖼️ Creative Gallery"])

with tab_upload:
    st.markdown("Upload your ad creative image to tag and score it.")
    uploaded = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "webp"], key="creative_upload")
    if uploaded:
        st.image(uploaded, caption=uploaded.name, width=400)
        c1, c2 = st.columns(2)
        genre = c1.selectbox("Genre", ["Action", "Animation", "Comedy", "Drama", "Sci-Fi", "Documentary"])
        mood = c2.selectbox("Mood", ["Adventurous", "Thrilling", "Magical", "Inspiring", "Fun", "Intense"])
        cta = st.text_input("Call-to-Action text", "Watch Now")
        if st.button("🔮 Predict Engagement Score"):
            score = np.random.uniform(62, 95)
            st.session_state["last_score"] = score
            _show_gauge(score)
    else:
        st.info("Upload an image to get started, or browse the gallery →")

with tab_gallery:
    st.markdown("#### 🖼️ Pre-loaded Cinematic Creatives")
    cols = st.columns(3)
    for idx, (name, info) in enumerate(PLACEHOLDER_CREATIVES.items()):
        with cols[idx % 3]:
            st.markdown(_placeholder_html(name, info), unsafe_allow_html=True)
            st.caption(f"{info['genre']} · {info['mood']} · CTA: *{info['cta']}*")

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDE-BY-SIDE COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### ⚔️ Side-by-Side Creative Comparison")
names = list(PLACEHOLDER_CREATIVES.keys())
c1, c2 = st.columns(2)
with c1:
    pick_a = st.selectbox("Creative A (Control)", names, index=0)
    st.markdown(_placeholder_html(pick_a, PLACEHOLDER_CREATIVES[pick_a], 320, 180), unsafe_allow_html=True)
with c2:
    pick_b = st.selectbox("Creative B (Variant)", names, index=1)
    st.markdown(_placeholder_html(pick_b, PLACEHOLDER_CREATIVES[pick_b], 320, 180), unsafe_allow_html=True)

if st.button("⚡ Compare Engagement Scores"):
    score_a = np.random.uniform(55, 85)
    score_b = np.random.uniform(60, 92)

    # animated gauge chart
    fig = go.Figure()
    for i, (label, score, color) in enumerate([
        (pick_a, score_a, BLUE), (pick_b, score_b, GOLD)
    ]):
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            title={"text": label, "font": {"size": 14, "color": "#ccc"}},
            delta={"reference": score_a if i == 1 else score_b, "relative": True,
                   "valueformat": ".1%"},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#555"},
                "bar": {"color": color},
                "bgcolor": "rgba(0,0,0,0)",
                "bordercolor": "rgba(255,255,255,0.1)",
                "steps": [
                    {"range": [0, 50], "color": "rgba(255,82,82,0.12)"},
                    {"range": [50, 75], "color": "rgba(255,215,0,0.08)"},
                    {"range": [75, 100], "color": "rgba(0,230,118,0.10)"},
                ],
            },
            domain={"row": 0, "column": i},
        ))
    fig.update_layout(
        grid={"rows": 1, "columns": 2, "pattern": "independent"},
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E8E8E8"),
        margin=dict(t=60, b=20, l=30, r=30),
    )
    st.plotly_chart(fig, use_container_width=True)

    winner = pick_b if score_b > score_a else pick_a
    lift = abs(score_b - score_a) / min(score_a, score_b) * 100
    st.success(f"🏆 **{winner}** wins with **{lift:.1f}%** higher engagement!")
    if lift > 10:
        st.balloons()
