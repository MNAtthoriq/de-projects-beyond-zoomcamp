"""
Frontend for streamlit app of this project
"""
from pathlib import Path
 
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
 
import core

# config
MODEL_PATH = Path(__file__).resolve().parent.parent / "bqml_model" / "xgb_bytes_predictor" / "model.bst"

BG_CARD = "#1E293B"      
BORDER = "#475569"       
TEXT_PRIMARY = "#E2E8F0" 
TEXT_MUTED = "#94A3B8"   
ACCENT_INDIGO = "#818CF8"
ACCENT_GREEN = "#34D399"

CHART_FONT = dict(
    family="Source Sans Pro, Source Sans 3, sans-serif", 
    color=TEXT_PRIMARY
)

# cache
@st.cache_resource
def load_model(path: Path):
    return core.load_booster(path)

@st.cache_data(ttl=3600)
def fetch_usd_idr_rate():
    return core.fetch_usd_idr_rate()

# page
st.set_page_config(
    page_title="Is Partition & Cluster Worth It?",
    page_icon="😮", layout="wide",
    initial_sidebar_state=350
)

st.markdown(
    f"""
    <style>
    .block-container {{ padding-top: 2rem; }}
    div[data-testid="stMetric"] {{
        background-color: {BG_CARD}; border: 1px solid {BORDER};
        border-radius: 10px; padding: 14px 16px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# header
st.title("Is Partitioning and Clustering Really Worth It?")
st.caption(
    "See how partitioning and clustering affect your BigQuery query cost. "
    "Compare bytes scanned and cost across storage strategies before execution. " \
    "Powered by BigQuery ML trained on 24,000+ real dry-run benchmarks across 12 months data."
)

# load model, if there is no model yet, you may upload .bst file
booster = load_model(MODEL_PATH)
if booster is None:
    st.warning(f"No model found at `{MODEL_PATH}`. Upload a `.bst` file to continue.")
    uploaded = st.file_uploader("Upload model.bst", type=["bst"])
    if uploaded is not None:
        tmp_path = Path("uploaded_model.bst")
        tmp_path.write_bytes(uploaded.read())
        booster = load_model(tmp_path)
    if booster is None:
        st.stop()

# sidebar input and credit
with st.sidebar:
    with st.expander("**DESCRIBE YOUR QUERY**", expanded=True):

        # table size
        st.caption("How big is your table?")
        table_size_gb = st.slider(
            "Table size",
            1.0, 7.0, 5.0, 0.5,
            "%.1f GB",
            label_visibility="collapsed"
        )

        # filter days
        st.caption("How many partition days your table filter?")
        filter_days = st.slider(
            "Filter days",
            1.0, 100.0, 10.0, 3.0,
            "%.0f%%",
            label_visibility="collapsed"
        )
        
        # filter zone
        st.caption("How many cluster zones your table filter?")
        filter_zones = st.slider(
            "Filter zones",
            1.0, 100.0, 10.0, 3.0,
            "%.0f%%",
            label_visibility="collapsed"
        )

		# queries per day
        st.caption("How many queries per day?")
        queries_per_day = st.number_input(
            "Queries per day", 
            1, None, 10000,
            label_visibility="collapsed"
        )
        
    with st.expander("**DESCRIBE YOUR CURRENCY**", expanded=False):
        st.caption("Enter cost/TiB scanned in:")
        input_currency = st.radio(
            "Enter cost/TiB in:", ["USD", "IDR"], 
            horizontal=True, label_visibility="collapsed"
        )
        usd_idr_rate = fetch_usd_idr_rate()
        default_input_price = (
            core.DEFAULT_PRICE_PER_TIB_USD
            if input_currency == "USD"
            else core.DEFAULT_PRICE_PER_TIB_USD * (usd_idr_rate or 18000)
        )
        st.caption(f"Enter cost/TiB scanned ({input_currency}):")
        price_per_tib_input = st.number_input(
            f"Cost per TiB scanned ({input_currency})",
            min_value=0.0, value=float(default_input_price),
            format="%.2f" if input_currency == "USD" else "%.0f",
            label_visibility="collapsed"
        )

        st.caption("Show cost result in:")
        display_currency = st.radio(
            "Show results in:", ["USD", "IDR"],
            horizontal=True, label_visibility="collapsed"
        )
    
        price_per_tib_display, conversion_ok = core.resolve_display_price(
            price_per_tib_input, input_currency, display_currency, usd_idr_rate
        )
        if not conversion_ok:
            st.caption("⚠️ Live USD/IDR rate unavailable right now. Showing results in your input currency instead.")
            display_currency = input_currency

    # credit
    st.markdown(
        f"""
        <div style="text-align:center; font-size:1em; color:{TEXT_MUTED}; line-height:1.6;">
            Built by <b style="color:{TEXT_PRIMARY};">MN Atthoriq</b><br>
            <a href="https://www.linkedin.com/in/mnatthoriq/" target="_blank" style="color:{ACCENT_INDIGO}; text-decoration:none;">LinkedIn</a>
            &nbsp;·&nbsp;
            <a href="https://github.com/MNAtthoriq/de-projects-beyond-zoomcamp/tree/main/03-data-warehouse" target="_blank" style="color:{ACCENT_INDIGO}; text-decoration:none;">GitHub</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# compute
table_size_bytes = table_size_gb * core.BYTES_PER_GB
partition_ratio = filter_days / 100
cluster_ratio = filter_zones / 100

# predict
raw_df = core.predict_bytes(booster, table_size_bytes, partition_ratio, cluster_ratio)
result_df = core.add_cost_and_saving(raw_df, price_per_tib_display)
best_row = result_df.iloc[-1]

# callout best strategy
if best_row["strategy"] != "No optimization" and best_row["saving_pct"] > 1:
    st.success(
        f"**\"{best_row['strategy']}\"** is the best strategy that cuts data scanned by **{best_row['saving_pct']:.2f}%**, "
        f"saving {core.format_money(best_row['saving_abs'], display_currency)} per query."
    )
else:
    st.info("For this parameter combination, optimization barely moves the needle. The baseline is already close to optimal.")

# scoreboard saving cost
per_query = best_row["saving_abs"]
c1, c2, c3 = st.columns(3)
c1.metric("Saving per day", core.format_money(per_query * queries_per_day, display_currency, 0))
c2.metric("Saving per month", core.format_money(per_query * queries_per_day * 30, display_currency, 0))
c3.metric("Saving per year", core.format_money(per_query * queries_per_day * 365, display_currency, 0))

# table
st.subheader("Strategy Breakdown")
table_view = result_df[["strategy", "predicted_bytes", "cost", "saving_pct", "saving_abs"]].copy()
table_view["predicted_bytes"] = table_view["predicted_bytes"].apply(core.format_bytes)
table_view["cost"] = table_view["cost"].apply(lambda c: core.format_money(c, display_currency))
table_view["saving_pct"] = table_view["saving_pct"].apply(lambda p: f"{p:.1f}%")
table_view["saving_abs"] = table_view["saving_abs"].apply(lambda a: core.format_money(a, display_currency))
table_view.columns = ["Strategy", "Data Scanned", "Cost / Query", "Cost Saving", "Saved / Query"]
st.dataframe(table_view, hide_index=True, width='stretch')

# barh
st.subheader("Cost Comparison")
bar_colors = [ACCENT_GREEN if s == best_row["strategy"] else TEXT_MUTED for s in result_df["strategy"]]
fig = go.Figure(
    go.Bar(
        x=result_df["cost"], y=result_df["strategy"],
        orientation="h", marker_color=bar_colors,
        customdata=[core.format_money(c, display_currency) for c in result_df["cost"]],
        hovertemplate="%{y}: %{customdata}<extra></extra>"
    )
)
fig.update_layout(
    xaxis_title=f"Cost per query ({display_currency})",
    showlegend=False, height=300,
    margin=dict(l=150, r=10, t=10, b=10),
    font=CHART_FONT,
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(color=TEXT_PRIMARY, gridcolor=BORDER),
    yaxis=dict(
        color=TEXT_PRIMARY, gridcolor=BORDER,
        automargin=True
    ),
)
fig.update_yaxes(autorange="reversed")
st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

# explanation
with st.expander("**ABOUT THIS TOOL**"):
    st.subheader("What is this?")
    st.markdown(
        """
        This tool answers: **"Is partitioning and clustering really worth it?"**

        It simulates BigQuery query costs using a BigQuery ML **XGBoost**. 
        
        Model trained on **12 months** real dataset of NYC Taxi with **24,000+** real dry-run benchmarks.
 
        **Query pattern:**
        ```sql
        SELECT COUNT(*) AS n
        FROM {table}
        WHERE {date_partition} AND {cluster_column} IN ({zone_list})
        ```

        **Download result** from benchmark run [here](https://raw.githubusercontent.com/MNAtthoriq/de-projects-beyond-zoomcamp/refs/heads/main/03-data-warehouse/results/benchmark_results.csv)
        """
    )
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Why the model thinks this?")
        imp_df = pd.DataFrame(sorted(core.FEATURE_IMPORTANCE.items(), key=lambda x: x[1]), columns=["feature", "importance"])
        fig2 = go.Figure(go.Bar(x=imp_df["importance"], y=imp_df["feature"], orientation="h", marker_color=ACCENT_INDIGO))
        fig2.update_layout(
            height=260, xaxis_title="Feature Importance", margin=dict(l=130, r=0, t=0, b=0),
            font=CHART_FONT,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(color=TEXT_PRIMARY, gridcolor=BORDER),
            yaxis=dict(color=TEXT_PRIMARY, gridcolor=BORDER),
        )
        st.plotly_chart(fig2, width="stretch")
    with col2:
        sc1, sc2 = st.columns([1, 1])
        with sc1:
            st.metric("Test R\u00b2", f"{core.MODEL_METRICS["r2_test"]:.4f}")
            st.metric("Test MAE", f"{core.MODEL_METRICS["mae_test_mb"]:.2f} MB")
        with sc2:
            st.metric("Train R\u00b2", f"{core.MODEL_METRICS["r2_train"]:.4f}")
            st.metric("Train MAE", f"{core.MODEL_METRICS["mae_train_mb"]:.2f} MB")
        fit = core.MODEL_METRICS["fit"]
        if fit == "good fit":
            st.success("✅ **Good fit**: generalizes well to unseen table sizes and date/zone combinations")
        elif fit == "overfit":
            st.warning("⚠️ **Overfit**: treat predictions with some caution")
        else:
            st.warning("⚠️ **Underfit**: model may be too simple for this relationship")
    
    st.markdown(
            """
            Feature importance reveals that bytes scanned are driven mainly by **storage design strategy** and **query selectivity**. 
            
            Partitioning, table size, and clustering consistently dominate the model's decisions, 
            showing that **thoughtful table design** can **significantly reduce** BigQuery costs.

            This answer that "partitioning and clustering are **really worth it**"
            """
        )














