# pages/5_🧪_SQL_Lab_&_Gallery.py — SQL Lab & Query Gallery
"""
DuckDB-powered in-browser SQL engine with 5 pre-loaded Disney-style
analytics queries + custom query editor + CSV export.
"""

import streamlit as st
import pandas as pd
import duckdb
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.viz import apply_global_css, hero_banner, styled_fig, GOLD, BLUE
from utils.data_generator import generate_ab_data
import plotly.express as px

st.set_page_config(page_title="🧪 SQL Lab", page_icon="🧪", layout="wide")
apply_global_css()

hero_banner("🧪 SQL Lab & Gallery", "Query experiment data with DuckDB — streaming analytics, Disney-style")

# ══════════════════════════════════════════════════════════════════════════════
# PREPARE DATA
# ══════════════════════════════════════════════════════════════════════════════
df = st.session_state.get("experiment_data")
if df is None:
    df = generate_ab_data(5000, 5000, 0.12, 0.02, "beta", 42)
    st.session_state["experiment_data"] = df

# register in DuckDB
con = duckdb.connect()
con.register("experiment", df)

# ══════════════════════════════════════════════════════════════════════════════
# PRE-LOADED QUERIES
# ══════════════════════════════════════════════════════════════════════════════
QUERIES = {
    "📊 Conversion Rate by Group": """
SELECT
    "group",
    COUNT(*) AS users,
    SUM(converted) AS conversions,
    ROUND(AVG(converted) * 100, 2) AS conversion_rate_pct,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM experiment
GROUP BY "group"
ORDER BY "group"
""",
    "🎬 Genre Performance (LTV Proxy)": """
SELECT
    genre,
    COUNT(*) AS users,
    ROUND(AVG(revenue), 2) AS avg_revenue,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(AVG(converted) * 100, 2) AS cvr_pct
FROM experiment
WHERE converted = 1
GROUP BY genre
ORDER BY avg_revenue DESC
""",
    "📱 Device × Plan Engagement Matrix": """
SELECT
    device,
    plan,
    COUNT(*) AS users,
    ROUND(AVG(converted) * 100, 2) AS cvr_pct,
    ROUND(AVG(revenue), 2) AS avg_rev
FROM experiment
GROUP BY device, plan
ORDER BY cvr_pct DESC
""",
    "📈 Daily Conversion Trend (Simulated)": """
SELECT
    CAST(timestamp AS DATE) AS day,
    "group",
    COUNT(*) AS users,
    SUM(converted) AS conversions,
    ROUND(AVG(converted) * 100, 3) AS cvr_pct
FROM experiment
GROUP BY day, "group"
ORDER BY day, "group"
""",
    "🏆 Top Regions by Revenue Uplift": """
WITH region_stats AS (
    SELECT
        region,
        "group",
        ROUND(AVG(revenue), 2) AS avg_rev,
        COUNT(*) AS n
    FROM experiment
    GROUP BY region, "group"
)
SELECT
    c.region,
    c.avg_rev AS control_rev,
    v.avg_rev AS variant_rev,
    ROUND(v.avg_rev - c.avg_rev, 2) AS rev_uplift,
    ROUND((v.avg_rev - c.avg_rev) / NULLIF(c.avg_rev, 0) * 100, 2) AS uplift_pct
FROM region_stats c
JOIN region_stats v ON c.region = v.region
WHERE c."group" = 'control' AND v."group" = 'variant'
ORDER BY uplift_pct DESC
""",
}

# ══════════════════════════════════════════════════════════════════════════════
# QUERY GALLERY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 📚 Pre-Loaded Query Gallery")
st.caption("Click any query to load it into the editor below")

gallery_cols = st.columns(3)
for idx, (name, sql) in enumerate(QUERIES.items()):
    with gallery_cols[idx % 3]:
        with st.container(border=True):
            if st.button(name, key=f"q_{idx}", use_container_width=True):
                st.session_state["sql_query"] = sql.strip()

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# QUERY EDITOR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### ✏️ SQL Editor")

default_query = st.session_state.get("sql_query", list(QUERIES.values())[0].strip())
query = st.text_area("Write your SQL (table: `experiment`)", value=default_query, height=180)

run_col, export_col = st.columns([1, 4])
run_clicked = run_col.button("▶️ Execute", type="primary")

if run_clicked and query.strip():
    try:
        result_df = con.execute(query).fetchdf()
        st.session_state["sql_result"] = result_df
        st.success(f"✅ Query returned **{len(result_df):,}** rows")
    except Exception as e:
        st.error(f"❌ Query error: {e}")

result_df = st.session_state.get("sql_result")
if result_df is not None:
    st.dataframe(result_df, use_container_width=True, height=350)

    # auto-visualise if small result set
    if len(result_df) <= 50 and len(result_df.columns) >= 2:
        st.markdown("#### 📊 Auto-Visualisation")
        num_cols = result_df.select_dtypes(include="number").columns.tolist()
        str_cols = result_df.select_dtypes(include="object").columns.tolist()

        if str_cols and num_cols:
            x_col = str_cols[0]
            y_col = num_cols[0]
            fig = px.bar(result_df, x=x_col, y=y_col,
                         color=str_cols[1] if len(str_cols) > 1 else None,
                         barmode="group", title=f"{y_col} by {x_col}")
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E8E8E8"),
            )
            st.plotly_chart(styled_fig(fig), use_container_width=True)

    # CSV export
    csv = result_df.to_csv(index=False)
    st.download_button("📥 Export to CSV", data=csv, file_name="query_result.csv", mime="text/csv")

st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#555;font-size:0.78rem;">
    Powered by <span style="color:#FFD700;">DuckDB</span> — blazing-fast in-process SQL engine<br>
    Table schema: experiment(user_id, group, converted, revenue, metric, genre, device, age_group, region, plan, creative, timestamp)
</div>
""", unsafe_allow_html=True)
