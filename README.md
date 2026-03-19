# ✨ Enchanted AdLab – MagicStream A/B Experiment Simulator

> **"Test blockbuster streaming ads like Disney DTC – Interactive • Statistical • Beautiful • Ready to impress recruiters"**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://enchanted-adlab.streamlit.app)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-FFD700?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-00BFFF?style=for-the-badge)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000?style=for-the-badge)](https://github.com/psf/black)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-FFD700?style=for-the-badge)](CONTRIBUTING.md)

---

<div align="center">

### 🎬 A cinematic-grade A/B testing platform built for streaming & entertainment analytics

*Imagine Disney's internal AdLab — but open-source, interactive, and running in your browser.*

**[🚀 Live Demo](https://enchanted-adlab.streamlit.app)** · **[📖 Documentation](#features)** · **[🐛 Report Bug](../../issues)** · **[💡 Request Feature](../../issues)**

</div>

---

## 🎥 Demo Preview

> **Screenshot / GIF goes here**
> Record with: `pip install streamlit-screenrecorder` or use [ScreenToGif](https://www.screentogif.com/)

```
┌─────────────────────────────────────────────────────────────────┐
│  ✨ ENCHANTED ADLAB                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │🎨 Studio │ │🔬 Sim    │ │📊 Analyze│ │📢 Story  │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  GLASSMORPHISM CARDS + PLOTLY CHARTS + LIVE METRICS     │    │
│  │  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │    │
│  │  Revenue Impact: $2.8M ↑  |  Statistical Power: 94%    │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🌟 Features

### 🎨 Page 1 — Ad Creative Studio
- Upload or select from **6 cinematic placeholder creatives**
- Side-by-side visual comparison with glassmorphism frames
- Tag creatives with genre, mood, CTA, and target audience
- Real-time engagement score prediction with animated gauges

### 🔬 Page 2 — Experiment Simulator
- Generate synthetic data via **Beta, Poisson, or Normal** distributions
- Configure sample sizes, effect sizes, and traffic splits interactively
- Watch experiments run with **animated progress bars + sparkle effects**
- Full frequentist engine: Z-test, T-test, Chi-squared (auto-selected)
- **Sample Ratio Mismatch (SRM)** detector with chi-squared goodness-of-fit
- **Bayesian Beta posteriors** with credible intervals + rope analysis
- Sequential testing with **always-valid p-values**

### 📊 Page 3 — Deep Analyzer
- **Segment-level heterogeneous treatment effects** (age, device, genre)
- **T-Learner uplift modeling** with scikit-learn
- **Multiple testing correction** (Bonferroni, Holm, BH-FDR)
- Interactive Plotly heatmaps, waterfalls, and funnel charts
- **Multi-Armed Bandit Arena** — epsilon-greedy live simulation with crown on winner

### 📢 Page 4 — Executive Storyteller
- **One-click executive summary** with auto-generated insights
- Real-time **revenue impact calculator**: users × lift × ARPU → animated $2.8M
- Downloadable markdown report styled as a "board deck"
- Fake PDF download button for portfolio demonstration

### 🧪 Page 5 — SQL Lab & Gallery
- **DuckDB-powered** in-browser SQL engine
- **5 pre-loaded Disney-style queries** (subscriber churn, ad impressions, genre LTV, etc.)
- Custom query editor with syntax highlighting
- Export results to CSV with one click

### 🚀 Page 6 — Learn & Impress
- **Skills mapping table**: every feature → Disney job requirement
- Interactive quiz: "Are you ready for this role?"
- Easter egg: Konami code triggers a confetti explosion
- Personal branding section with contact links

---

## 🏗️ Architecture

```
enchanted-adlab/
├── .streamlit/config.toml    # Dark cinematic theme
├── app.py                     # Main entry + sidebar navigation
├── pages/
│   ├── 1_🎨_Ad_Creative_Studio.py
│   ├── 2_🔬_Experiment_Simulator.py
│   ├── 3_📊_Deep_Analyzer.py
│   ├── 4_📢_Executive_Storyteller.py
│   ├── 5_🧪_SQL_Lab_&_Gallery.py
│   └── 6_🚀_Learn_&_Impress.py
├── utils/
│   ├── data_generator.py      # Synthetic data (Beta/Poisson/Normal)
│   ├── stats_engine.py        # Frequentist + Bayesian + sequential
│   └── viz.py                 # Plotly chart factory + custom CSS
├── sample_data.csv
├── requirements.txt
├── Dockerfile
├── .gitignore
└── CONTRIBUTING.md
```

---

## ⚡ Quick Start

```bash
# Clone the repository
git clone https://github.com/YashpalSingh/enchanted-adlab.git
cd enchanted-adlab

# Create virtual environment
python -m venv venv && source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch the magic
streamlit run app.py
```

Open **http://localhost:8501** and explore the cinematic dashboard.

---

## 🐳 Docker

```bash
docker build -t enchanted-adlab .
docker run -p 8501:8501 enchanted-adlab
```

---

## ☁️ Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Select your repo → `app.py` → Deploy
4. Share the link on LinkedIn with: *"I built Disney's internal AdLab. Here's the open-source version."*

---

## 🎯 How This Gets Me Hired

| Disney Job Requirement | Enchanted AdLab Feature | Page |
|---|---|---|
| Design & analyze A/B tests | Full frequentist + Bayesian simulator | 🔬 Simulator |
| Statistical significance & power analysis | Auto Z/T/Chi² + sample size calculator | 🔬 Simulator |
| SQL for large datasets | DuckDB SQL Lab with 5 production queries | 🧪 SQL Lab |
| Data visualization & storytelling | 15+ Plotly chart types + exec summary | 📊 Analyzer, 📢 Storyteller |
| Revenue impact quantification | Real-time ARPU × lift calculator ($2.8M) | 📢 Storyteller |
| Segment-level analysis | T-Learner uplift + heterogeneous effects | 📊 Analyzer |
| Cross-functional communication | One-click executive deck generator | 📢 Storyteller |
| Python, pandas, statistical modeling | 2,000+ lines of production Python | Everywhere |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Streamlit 1.42** | Interactive web framework |
| **Plotly 6.0** | All charts (zero matplotlib) |
| **SciPy + Statsmodels** | Frequentist statistical tests |
| **NumPy** | Bayesian posterior sampling |
| **Scikit-learn** | T-Learner uplift modeling |
| **DuckDB** | In-browser SQL engine |
| **Pandas** | Data manipulation |
| **Pillow** | Image processing |

---

## 📬 Contact

**Yashpal** — Data Analyst who builds tools, not just dashboards.

- 🔗 [LinkedIn](https://linkedin.com/in/yashpal)
- 💻 [GitHub](https://github.com/yashpal)
- 📧 yashpal@email.com

---

<div align="center">

*Built with ✨ magic and 🔬 statistics.*

**If this repo helped you, please ⭐ star it — it helps others discover it!**

</div>
