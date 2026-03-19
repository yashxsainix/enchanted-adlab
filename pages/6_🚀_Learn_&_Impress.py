# pages/6_🚀_Learn_&_Impress.py — Learn & Impress
"""
Skills mapping to Disney job requirements, interactive quiz,
Easter egg, and personal branding.
"""

import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.viz import apply_global_css, hero_banner, GOLD, BLUE, SUCCESS

st.set_page_config(page_title="🚀 Learn & Impress", page_icon="🚀", layout="wide")
apply_global_css()

hero_banner("🚀 Learn & Impress", "How this project maps 1:1 to the Disney Associate Data Analyst role")

# ══════════════════════════════════════════════════════════════════════════════
# SKILLS MAPPING TABLE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🎯 Skills Mapping — Every Feature = A Job Requirement")

skills = [
    ("Design & analyse A/B tests",
     "Full frequentist + Bayesian experiment simulator with SRM detection",
     "🔬 Simulator", "⭐⭐⭐⭐⭐"),
    ("Statistical significance & power analysis",
     "Auto Z/T/Chi² selection, power calculator, sequential testing",
     "🔬 Simulator", "⭐⭐⭐⭐⭐"),
    ("SQL for large datasets",
     "DuckDB SQL Lab with 5 production-grade streaming queries",
     "🧪 SQL Lab", "⭐⭐⭐⭐⭐"),
    ("Data visualisation & storytelling",
     "15+ Plotly chart types, glassmorphism dashboard, exec summary generator",
     "📊 Analyzer + 📢 Storyteller", "⭐⭐⭐⭐⭐"),
    ("Revenue impact quantification",
     "Real-time ARPU × lift calculator projecting $2.8M+ annual impact",
     "📢 Storyteller", "⭐⭐⭐⭐⭐"),
    ("Segment-level analysis",
     "T-Learner uplift modelling + heterogeneous treatment effects by 5 dimensions",
     "📊 Deep Analyzer", "⭐⭐⭐⭐⭐"),
    ("Cross-functional communication",
     "One-click executive deck with auto-generated narrative + download",
     "📢 Storyteller", "⭐⭐⭐⭐"),
    ("Python & statistical modelling",
     "2,500+ lines: SciPy, statsmodels, scikit-learn, numpy, pandas",
     "Everywhere", "⭐⭐⭐⭐⭐"),
    ("Experimentation best practices",
     "SRM checks, multiple testing correction, Bayesian decision rules",
     "🔬 + 📊", "⭐⭐⭐⭐⭐"),
    ("Multi-armed bandits & adaptive testing",
     "Epsilon-greedy simulation arena with live reward tracking",
     "📊 Deep Analyzer", "⭐⭐⭐⭐"),
]

for req, feature, page, rating in skills:
    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 4, 2])
        c1.markdown(f"**{req}**")
        c2.markdown(f"{feature}")
        c3.markdown(f"{page} {rating}")

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE QUIZ
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🧠 Quiz — Are You Ready for This Role?")

if "quiz_score" not in st.session_state:
    st.session_state["quiz_score"] = None
    st.session_state["quiz_submitted"] = False

questions = [
    {
        "q": "What test should you use for comparing two proportions?",
        "options": ["T-test", "Z-test for proportions", "ANOVA", "Mann-Whitney U"],
        "answer": 1,
    },
    {
        "q": "What does SRM stand for in A/B testing?",
        "options": ["Statistical Regression Model", "Sample Ratio Mismatch",
                     "Sequential Random Method", "Standard Rate Metric"],
        "answer": 1,
    },
    {
        "q": "In Bayesian A/B testing, what distribution models binary conversion?",
        "options": ["Normal", "Poisson", "Beta", "Gamma"],
        "answer": 2,
    },
    {
        "q": "What correction method controls the False Discovery Rate?",
        "options": ["Bonferroni", "Holm", "Benjamini-Hochberg", "Šidák"],
        "answer": 2,
    },
    {
        "q": "What does epsilon control in epsilon-greedy bandits?",
        "options": ["Learning rate", "Exploration rate", "Discount factor", "Batch size"],
        "answer": 1,
    },
]

answers = []
for i, q in enumerate(questions):
    st.markdown(f"**Q{i+1}. {q['q']}**")
    ans = st.radio("", q["options"], key=f"quiz_{i}", index=None, label_visibility="collapsed")
    answers.append(ans)

if st.button("📝 Submit Quiz", key="submit_quiz"):
    score = 0
    for i, q in enumerate(questions):
        if answers[i] == q["options"][q["answer"]]:
            score += 1
    st.session_state["quiz_score"] = score
    st.session_state["quiz_submitted"] = True

if st.session_state.get("quiz_submitted"):
    score = st.session_state["quiz_score"]
    total = len(questions)
    pct = score / total * 100

    if pct == 100:
        st.success(f"🏆 Perfect score! {score}/{total} — You're Disney-ready! 🎉")
        st.balloons()
    elif pct >= 60:
        st.info(f"👍 Good job! {score}/{total} — Review the pages for the ones you missed.")
    else:
        st.warning(f"📚 {score}/{total} — Explore the simulator pages to level up!")

    # show correct answers
    with st.expander("📖 See correct answers"):
        for i, q in enumerate(questions):
            correct = q["options"][q["answer"]]
            given = answers[i] or "No answer"
            icon = "✅" if given == correct else "❌"
            st.markdown(f"{icon} **Q{i+1}**: {correct}")

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# EASTER EGG
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🥚 Easter Egg")
st.caption("Type the magic word to unlock a surprise...")

magic = st.text_input("🔮 Enter the magic word:", key="easter_egg", label_visibility="visible")
if magic.lower() in ["disney", "magic", "enchanted", "adlab", "yashpal"]:
    st.balloons()
    st.markdown(f"""
    <div style="text-align:center;padding:30px;background:linear-gradient(135deg,rgba(255,215,0,0.12),rgba(0,191,255,0.08));
         border:1px solid rgba(255,215,0,0.2);border-radius:18px;margin:16px 0;">
        <div style="font-size:3rem;">🏰✨🎆</div>
        <div style="font-family:'Playfair Display',serif;font-size:1.8rem;
             background:linear-gradient(135deg,#FFD700,#00BFFF);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             font-weight:700;margin:10px 0;">
            You Found the Magic!
        </div>
        <div style="color:#ccc;font-size:0.95rem;max-width:500px;margin:0 auto;">
            Every great product starts with curiosity.
            This entire platform was built to demonstrate that data analysis
            is not just about numbers — it's about telling stories that drive decisions.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PERSONAL BRANDING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 👤 About the Builder")

st.markdown(f"""
<div style="background:rgba(20,20,20,0.85);border:1px solid rgba(255,215,0,0.12);
     border-radius:16px;padding:28px 32px;max-width:600px;margin:0 auto;">
    <div style="text-align:center;">
        <div style="font-size:3rem;margin-bottom:8px;">🧑‍💻</div>
        <div style="font-family:'Playfair Display',serif;font-size:1.5rem;
             color:#FFD700;font-weight:700;">Yashpal</div>
        <div style="color:#999;font-size:0.88rem;margin-top:4px;">
            Data Analyst · Experimentation Enthusiast · Builder
        </div>
    </div>
    <div style="margin-top:16px;color:#bbb;font-size:0.88rem;line-height:1.6;">
        I don't just analyse data — I build tools that make data analysis accessible,
        beautiful, and actionable. This project demonstrates my ability to:
    </div>
    <ul style="color:#bbb;font-size:0.85rem;margin-top:10px;line-height:1.8;">
        <li>Design and execute A/B experiments end-to-end</li>
        <li>Apply both frequentist and Bayesian statistics rigorously</li>
        <li>Write production-grade Python with clean architecture</li>
        <li>Build interactive data products from scratch</li>
        <li>Translate technical results into executive narratives</li>
    </ul>
    <div style="text-align:center;margin-top:20px;">
        <span class="badge badge-gold">Python</span>
        <span class="badge badge-blue">Statistics</span>
        <span class="badge badge-gold">A/B Testing</span>
        <span class="badge badge-blue">SQL</span>
        <span class="badge badge-gold">Streamlit</span>
        <span class="badge badge-blue">Plotly</span>
    </div>
    <div style="text-align:center;margin-top:16px;">
        <a href="https://linkedin.com/in/yashpal" style="color:#00BFFF;text-decoration:none;margin:0 12px;">🔗 LinkedIn</a>
        <a href="https://github.com/yashpal" style="color:#FFD700;text-decoration:none;margin:0 12px;">💻 GitHub</a>
        <a href="mailto:yashpal@email.com" style="color:#ccc;text-decoration:none;margin:0 12px;">📧 Email</a>
    </div>
</div>
""", unsafe_allow_html=True)
