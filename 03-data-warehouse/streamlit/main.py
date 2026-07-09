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
    initial_sidebar_state=450
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

st.title("Is Partitioning and Clustering Really Worth It?")
st.caption(
    "See how partitioning and clustering affect your BigQuery query cost. "
    "Compare bytes scanned and cost across storage strategies before execution. " \
    "Powered by BigQuery ML trained on 4,000+ real dry-run benchmarks across 12 months data."
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

with st.sidebar:
    with st.expander("**DESCRIBE YOUR QUERY**", expanded=True):

        # table size
        st.caption("How big is your table?")
        table_size_gb = st.slider(
            "Table size",
            0.5, 30.0, 5.0, 0.5,
            "%.1f GB",
            label_visibility="collapsed"
        )
        if table_size_gb > core.TRAIN_SIZE_GB_MAX * 1.5:
            st.caption(
                f"⚠️ Training data only covered "
                f"{core.TRAIN_SIZE_GB_MIN:.1f} - {core.TRAIN_SIZE_GB_MAX:.1f} GB tables. "
                "Treat this as a rough extrapolation, not a precise estimate."
            )
        
        # total days
        st.caption("How many days your table cover?")
        total_days = st.number_input(
            "Total days",
            1, None, 100,
            label_visibility="collapsed",
        )
        if total_days > core.TRAIN_SIZE_DAYS_MAX * 1.5 and total_days <= 4000:
            st.caption(
                f"⚠️ Training data only covered "
                f"{core.TRAIN_SIZE_DAYS_MIN} - {core.TRAIN_SIZE_DAYS_MAX} total days. "
                "Treat this as a rough extrapolation, not a precise estimate."
            )
        if total_days > 4000:
            st.caption(" :red[⚠️ Maximum days reached! \nYou cannot exceed 4000 days.]")
            total_days = None

        # filter days
        st.caption("How many days your table filter?")
        filter_days = st.number_input(
            "Filter days",
            1, None, min(7, int(total_days)),
            label_visibility="collapsed"
        )
        if filter_days > int(total_days):
            st.caption(f" :red[⚠️ Maximum days reached! \nYou cannot exceed {int(total_days)} total days.]")
            filter_days = None
        
        # filter zone
        st.caption("How many pickup zones your table filter?")
        filter_zones = st.number_input(
            "Filter zone",
            1, None, 10,
            label_visibility="collapsed"
        )
        if filter_zones > core.TOTAL_ZONES:
            st.caption(f" :red[⚠️ Maximum zone reached! \nYou cannot exceed {core.TOTAL_ZONES} zone.]")
            filter_zones = None

        # calculate ratio
        partition_ratio = filter_days / total_days
        cluster_ratio = filter_zones / core.TOTAL_ZONES
        st.caption("How many queries per day?")
        queries_per_day = st.number_input(
            "Queries per day", 
            1, None, 100,
            label_visibility="collapsed"
        )
        
    with st.expander("**DESCRIBE YOUR CURRENCY**", expanded=True):
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