<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6B21A8,50:7C3AED,100:8B5CF6&height=220&section=header&text=Statistical+A%2FB+Testing+Platform&fontSize=44&fontColor=fff&animation=twinkling&fontAlignY=38&desc=Live+Streamlit+App+%E2%80%A2+Claude+API+%E2%80%A2+Automated+Statistical+Narratives&descAlignY=62&descSize=18" />

<br/>

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=1000&color=A78BFA&center=true&vCenter=true&width=750&lines=Live+Demo+Running+in+Your+Browser+Right+Now;Z-test+%2B+T-test+%2B+Chi-squared+%E2%80%94+Auto-selected;Claude+API+Generates+Plain-English+Experiment+Summaries;Non-Technical+Teams+Run+Rigorous+Experiments+Without+Help)](https://yashpal-adlab.streamlit.app)

<br/>

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-yashpal--adlab.streamlit.app-7C3AED?style=for-the-badge)](https://yashpal-adlab.streamlit.app)

<br/>

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Claude API](https://img.shields.io/badge/Claude_API-Anthropic-D97706?style=for-the-badge)](https://anthropic.com)
[![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?style=for-the-badge&logo=scipy&logoColor=white)](https://scipy.org)
[![SQL](https://img.shields.io/badge/SQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)

<br/>

<img src="https://img.shields.io/badge/Status-Live-3FB950?style=flat-square&labelColor=0D1117" />
<img src="https://img.shields.io/badge/Statistical_Tests-3_Methods-7C3AED?style=flat-square&labelColor=0D1117" />
<img src="https://img.shields.io/badge/AI_Narration-Claude_API-D97706?style=flat-square&labelColor=0D1117" />
<img src="https://img.shields.io/badge/SRM_Detection-Built_In-58A6FF?style=flat-square&labelColor=0D1117" />

</div>

---

## 🎯 The Problem

Running a statistically rigorous A/B test requires selecting the right statistical test, setting appropriate significance thresholds, detecting sample ratio mismatches, and then explaining what the results actually mean — all before you can act on the findings.

Most teams either skip the rigor and make bad decisions, or wait for an analyst to process the request.

This platform removes that bottleneck entirely. Upload your data, configure the experiment, and the platform runs the analysis and writes the explanation automatically.

---

## ✨ What It Does

```mermaid
graph LR
    A["📊 Upload Data\nor use sample dataset"] --> B["⚙️ Configure\nSignificance level\nTraffic split\nMetric type"]
    B --> C["🔬 Statistical Engine\nAuto-selects test:\n• Z-test (proportions)\n• T-test (means)\n• Chi-squared (categorical)"]
    C --> D["🚨 SRM Detection\nSample Ratio Mismatch\nchi-squared goodness-of-fit"]
    C --> E["🤖 Claude API\nGenerates plain-English\nexperiment narrative"]
    D --> F["📋 Results Report\nP-value · Effect size\nConfidence intervals\nPower analysis"]
    E --> F

    style A fill:#7C3AED,color:#fff,stroke:#7C3AED
    style C fill:#6B21A8,color:#fff,stroke:#6B21A8
    style E fill:#D97706,color:#fff,stroke:#D97706
    style F fill:#3FB950,color:#fff,stroke:#3FB950
```

---

## 🧪 Six Pages, One Platform

| Page | What It Does |
|------|-------------|
| 🎨 **Ad Creative Studio** | Upload or select test creatives, tag with genre/mood/CTA, real-time engagement score prediction |
| 🔬 **Experiment Simulator** | Generate synthetic data, configure sample sizes and effect sizes, watch experiments run |
| 📊 **Deep Analyzer** | Upload your own CSV, run full statistical analysis, get SRM detection automatically |
| 📢 **Executive Storyteller** | Claude API writes plain-English narrative from your results — ready to paste into a deck |
| 🧪 **SQL Lab & Gallery** | Query experiment data directly with SQL, browse historical experiments |
| 🚀 **Learn & Impress** | Interactive explainer of statistical concepts for non-technical teams |

---

## 🤖 The Claude API Integration

The most distinctive feature is automatic narrative generation. After the statistical engine computes results, the platform sends structured experiment data to Claude API and receives a plain-English summary that non-technical stakeholders can actually read.

```python
# Example output from Claude API narration:

"""
Variant B showed a statistically significant lift of 3.2 percentage points
in click-through rate (p=0.023, 95% CI: [0.4%, 6.0%]). With 94% statistical
power and no sample ratio mismatch detected, these results are reliable.

Recommendation: Roll out Variant B to 100% of traffic. At current volume,
this improvement corresponds to approximately 1,400 additional clicks per week.
"""
```

---

## 📐 Statistical Engine

The platform auto-selects the appropriate test based on your metric type:

| Metric Type | Test Used | When |
|-------------|-----------|------|
| Conversion rate / proportion | **Z-test** | Comparing two proportions |
| Revenue / continuous metric | **T-test (Welch's)** | Comparing two means |
| Categorical distribution | **Chi-squared** | Multi-cell frequency comparison |

**Sample Ratio Mismatch (SRM) Detection** runs automatically before results are displayed. An SRM occurs when the actual traffic split differs from the intended split — which invalidates the experiment entirely. The platform catches this before you act on bad data.

---

## 🔬 Statistical Rigor Built In

```python
# What runs under the hood on every experiment:

from scipy import stats

# 1. Auto-select test
test = select_test(metric_type, sample_sizes)

# 2. Run analysis
result = test.run(control, treatment, alpha=0.05)

# 3. Compute effect size (Cohen's d / relative lift)
effect = compute_effect_size(control, treatment)

# 4. Post-hoc power analysis
power = compute_power(effect, sample_sizes, alpha)

# 5. SRM check
srm_result = chi2_goodness_of_fit(actual_split, intended_split)

# 6. Send to Claude API for narrative
narrative = generate_narrative(result, effect, power, srm_result)
```

---

## 🚀 Run It Yourself

**Option 1 — Live Demo (no setup)**
👉 [yashpal-adlab.streamlit.app](https://yashpal-adlab.streamlit.app)

**Option 2 — Local**
```bash
git clone https://github.com/yashxsainix/enchanted-adlab
pip install -r requirements.txt

# Add your Claude API key
export ANTHROPIC_API_KEY="your-key-here"

streamlit run app.py
```

---

## 💡 Why This Exists

Most analyst time spent on A/B tests goes to setup, test selection, and writing the results summary — not to the actual statistical computation. This platform automates the mechanical parts so analysts can focus on experiment design and business interpretation.

The Claude API integration is not a gimmick. It is the difference between a result that sits in a spreadsheet and one that gets presented to leadership.

---

## 👤 Author

**Yashpal Saini** · [LinkedIn](https://linkedin.com/in/yash-saini-analyst) · [Portfolio](https://yashxsainix.github.io)

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6B21A8,50:7C3AED,100:8B5CF6&height=100&section=footer" />
