# utils/viz.py — Plotly chart factory + custom CSS injection for Enchanted AdLab
"""
Central theming module. Every visual element in the app flows through here
so the entire UI stays cohesive: dark cinematic background, gold + Disney-blue accents,
glassmorphism cards, and sparkle particle effects.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# ── colour palette ────────────────────────────────────────────────────────────
GOLD = "#FFD700"
BLUE = "#00BFFF"
BG_DARK = "#0A0A0A"
CARD_BG = "rgba(20,20,20,0.85)"
TEXT = "#E8E8E8"
SUCCESS = "#00E676"
DANGER = "#FF5252"
PURPLE = "#BB86FC"
GRADIENT_GOLD = "linear-gradient(135deg, #FFD700 0%, #FFA000 100%)"
GRADIENT_BLUE = "linear-gradient(135deg, #00BFFF 0%, #0077B6 100%)"

PLOTLY_TEMPLATE = dict(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color=TEXT, size=13),
        title_font=dict(size=18, color=GOLD),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.08)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.08)"),
        colorway=[GOLD, BLUE, SUCCESS, PURPLE, DANGER, "#FF9800", "#26C6DA", "#AB47BC"],
        margin=dict(l=40, r=20, t=50, b=40),
        hoverlabel=dict(bgcolor="#1E1E1E", font_color=TEXT, bordercolor=GOLD),
    )
)


def apply_global_css():
    """Inject the full custom stylesheet + sparkle particle JS into the page."""
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown(_SPARKLE_JS, unsafe_allow_html=True)


# ── glassmorphism CSS ─────────────────────────────────────────────────────────
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Playfair+Display:wght@700&display=swap');

/* ---- global overrides ---- */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0A0A0A !important;
    color: #E8E8E8 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F0F0F 0%, #0A0A0A 100%) !important;
    border-right: 1px solid rgba(255,215,0,0.12) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] .stMarkdown { color: #E8E8E8 !important; }

/* ---- glassmorphism card ---- */
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background: rgba(20,20,20,0.80) !important;
    border: 1px solid rgba(255,215,0,0.10) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.45) !important;
    transition: box-shadow 0.3s ease, border-color 0.3s ease !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {
    border-color: rgba(255,215,0,0.28) !important;
    box-shadow: 0 12px 48px rgba(255,215,0,0.08) !important;
}

/* ---- metric cards ---- */
[data-testid="stMetric"] {
    background: rgba(255,215,0,0.04);
    border: 1px solid rgba(255,215,0,0.12);
    border-radius: 12px;
    padding: 12px 16px;
    transition: transform 0.2s ease;
}
[data-testid="stMetric"]:hover { transform: translateY(-2px); }
[data-testid="stMetricValue"] { color: #FFD700 !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] svg { display: none; }

/* ---- tabs ---- */
button[data-baseweb="tab"] {
    background: transparent !important;
    color: #888 !important;
    border-bottom: 2px solid transparent !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #FFD700 !important;
    border-bottom: 2px solid #FFD700 !important;
}

/* ---- buttons ---- */
.stButton > button {
    background: linear-gradient(135deg, #FFD700 0%, #FFA000 100%) !important;
    color: #0A0A0A !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.6rem !important;
    box-shadow: 0 4px 18px rgba(255,215,0,0.18) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 24px rgba(255,215,0,0.30) !important;
}
.stButton > button:active { transform: scale(0.97) !important; }

/* ---- download button ---- */
.stDownloadButton > button {
    background: linear-gradient(135deg, #00BFFF 0%, #0077B6 100%) !important;
    color: #fff !important;
}

/* ---- sliders ---- */
[data-testid="stSlider"] [role="slider"] {
    background: #FFD700 !important;
    border-color: #FFD700 !important;
}

/* ---- progress bar ---- */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #FFD700, #00BFFF) !important;
}

/* ---- expander ---- */
details[data-testid="stExpander"] {
    border: 1px solid rgba(0,191,255,0.15) !important;
    border-radius: 12px !important;
    background: rgba(0,191,255,0.03) !important;
}

/* ---- selectbox / multiselect ---- */
[data-baseweb="select"] { border-color: rgba(255,215,0,0.18) !important; }

/* ---- hero title helper ---- */
.hero-title {
    font-family: 'Playfair Display', serif;
    background: linear-gradient(135deg, #FFD700 0%, #00BFFF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.6rem;
    font-weight: 700;
    line-height: 1.15;
    margin-bottom: 0.2rem;
}
.hero-sub {
    color: #999;
    font-size: 1.05rem;
    margin-bottom: 1.2rem;
}
.gold-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #FFD700, transparent);
    margin: 1.2rem 0;
    border: none;
}
.badge-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 0.8rem; }
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.badge-gold { background: rgba(255,215,0,0.12); color: #FFD700; border: 1px solid rgba(255,215,0,0.25); }
.badge-blue { background: rgba(0,191,255,0.10); color: #00BFFF; border: 1px solid rgba(0,191,255,0.22); }

/* ---- sparkle canvas ---- */
#sparkle-canvas {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    pointer-events: none; z-index: 9999;
}
</style>
"""

# ── sparkle particle effect (JS) ─────────────────────────────────────────────
_SPARKLE_JS = """
<canvas id="sparkle-canvas"></canvas>
<script>
(function(){
    const c = document.getElementById('sparkle-canvas');
    if (!c) return;
    const ctx = c.getContext('2d');
    let W, H, particles = [];
    function resize(){ W = c.width = window.innerWidth; H = c.height = window.innerHeight; }
    resize(); window.addEventListener('resize', resize);
    function Particle(){
        this.x = Math.random()*W; this.y = Math.random()*H;
        this.vx = (Math.random()-0.5)*0.3; this.vy = (Math.random()-0.5)*0.3;
        this.r = Math.random()*1.5+0.5;
        this.alpha = Math.random()*0.4+0.1;
        this.decay = 0.0005+Math.random()*0.001;
        this.color = Math.random()>0.5 ? '#FFD700' : '#00BFFF';
    }
    for(let i=0;i<40;i++) particles.push(new Particle());
    function draw(){
        ctx.clearRect(0,0,W,H);
        particles.forEach(p=>{
            p.x+=p.vx; p.y+=p.vy; p.alpha-=p.decay;
            if(p.alpha<=0){ Object.assign(p, new Particle()); p.alpha=Math.random()*0.4+0.1; }
            ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
            ctx.fillStyle=p.color; ctx.globalAlpha=p.alpha; ctx.fill();
        });
        ctx.globalAlpha=1;
        requestAnimationFrame(draw);
    }
    draw();
})();
</script>
"""


# ── Plotly chart helpers ──────────────────────────────────────────────────────

def styled_fig(fig: go.Figure, height: int = 420) -> go.Figure:
    """Apply the global dark cinematic template to any Plotly figure."""
    fig.update_layout(
        **PLOTLY_TEMPLATE["layout"].to_plotly_json(),
        height=height,
    )
    return fig


def distribution_chart(x_control, x_variant, title="Distribution Comparison"):
    """Overlayed histograms for control vs variant."""
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=x_control, name="Control (A)", opacity=0.65,
        marker_color=BLUE, nbinsx=50,
    ))
    fig.add_trace(go.Histogram(
        x=x_variant, name="Variant (B)", opacity=0.65,
        marker_color=GOLD, nbinsx=50,
    ))
    fig.update_layout(barmode="overlay", title=title)
    return styled_fig(fig)


def bayesian_posterior_chart(alpha_a, beta_a, alpha_b, beta_b):
    """Plot Beta posteriors for control and variant with shaded credible interval."""
    from scipy.stats import beta as beta_dist
    x = np.linspace(0, 1, 500)
    y_a = beta_dist.pdf(x, alpha_a, beta_a)
    y_b = beta_dist.pdf(x, alpha_b, beta_b)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y_a, fill="tozeroy", name="Control (A)",
                             line=dict(color=BLUE, width=2), fillcolor="rgba(0,191,255,0.18)"))
    fig.add_trace(go.Scatter(x=x, y=y_b, fill="tozeroy", name="Variant (B)",
                             line=dict(color=GOLD, width=2), fillcolor="rgba(255,215,0,0.18)"))
    fig.update_layout(title="Bayesian Beta Posteriors", xaxis_title="Conversion Rate", yaxis_title="Density")
    return styled_fig(fig)


def funnel_chart(stages: list[str], values: list[float], title="Conversion Funnel"):
    """Horizontal funnel using Plotly."""
    fig = go.Figure(go.Funnel(
        y=stages, x=values,
        textinfo="value+percent initial",
        marker=dict(color=[GOLD, BLUE, SUCCESS, PURPLE, DANGER][:len(stages)]),
        connector=dict(line=dict(color="rgba(255,255,255,0.1)", width=1)),
    ))
    fig.update_layout(title=title)
    return styled_fig(fig, height=360)


def bandit_chart(rewards_history: dict, title="Multi-Armed Bandit — Cumulative Rewards"):
    """Line chart showing cumulative reward per arm over time."""
    fig = go.Figure()
    colors = [GOLD, BLUE, SUCCESS, PURPLE, DANGER]
    for idx, (arm, vals) in enumerate(rewards_history.items()):
        fig.add_trace(go.Scatter(
            y=np.cumsum(vals), mode="lines", name=arm,
            line=dict(color=colors[idx % len(colors)], width=2),
        ))
    fig.update_layout(title=title, xaxis_title="Round", yaxis_title="Cumulative Reward")
    return styled_fig(fig)


def waterfall_chart(categories, values, title="Segment Uplift Waterfall"):
    """Waterfall chart for segment-level contribution."""
    measure = ["relative"] * len(values)
    fig = go.Figure(go.Waterfall(
        orientation="v", measure=measure,
        x=categories, y=values,
        connector=dict(line=dict(color="rgba(255,255,255,0.15)")),
        increasing=dict(marker=dict(color=SUCCESS)),
        decreasing=dict(marker=dict(color=DANGER)),
    ))
    fig.update_layout(title=title)
    return styled_fig(fig)


def kpi_card_html(label: str, value: str, delta: str = "", icon: str = "✨") -> str:
    """Return an HTML block for a fancy metric card (use with st.markdown unsafe)."""
    delta_color = SUCCESS if delta.startswith("+") else DANGER if delta.startswith("-") else TEXT
    return f"""
    <div style="background:rgba(20,20,20,0.85);border:1px solid rgba(255,215,0,0.12);
    border-radius:14px;padding:18px 22px;text-align:center;backdrop-filter:blur(10px);">
        <div style="font-size:1.6rem;margin-bottom:4px;">{icon}</div>
        <div style="color:#999;font-size:0.82rem;text-transform:uppercase;letter-spacing:0.06em;">{label}</div>
        <div style="color:#FFD700;font-size:1.7rem;font-weight:700;margin:4px 0;">{value}</div>
        <div style="color:{delta_color};font-size:0.85rem;font-weight:600;">{delta}</div>
    </div>"""


def hero_banner(title: str, subtitle: str):
    """Render the page hero with gradient title."""
    st.markdown(f'<div class="hero-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-sub">{subtitle}</div>', unsafe_allow_html=True)
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
