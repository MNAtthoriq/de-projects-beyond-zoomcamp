from __future__ import annotations
 
from pathlib import Path
 
import numpy as np
import pandas as pd
import requests
import xgboost as xgb

# config
FEATURES = ["has_partition", "has_cluster", "table_size_bytes", "partition_filter_ratio", "cluster_filter_ratio"]
FEATURE_IMPORTANCE = {
    "has_cluster": 0.4096,
    "has_partition": 0.2321,
    "table_size_bytes": 0.1793,
    "partition_filter_ratio": 0.1744,
    "cluster_filter_ratio": 0.0046,
} # write manual from feature_importance_bqml_model.sql query

MODEL_METRICS = {
    "r2_train": 0.9999,
    "r2_test": 0.9997,
    "r2_gap_pct": 0.0151,
    "mae_train_mb": 1.1978,
    "mae_test_mb": 2.0182,
    "mae_gap_pct": 68.4858,
    "fit": "good fit",
} # write manual from evaluate_bqml_model.sql query
MODEL_R2 = MODEL_METRICS["r2_test"]
MODEL_MAE_MB = MODEL_METRICS["mae_test_mb"]

TRAIN_SIZE_GB_MIN, TRAIN_SIZE_GB_MAX = 1.2, 7.3 # outside this range are extrapolation
TRAIN_SIZE_DAYS_MIN, TRAIN_SIZE_DAYS_MAX = 60, 365 # outside this range are extrapolation
DEFAULT_PRICE_PER_TIB_USD = 6.25  # BigQuery on-demand pricing, as of this build
BYTES_PER_TIB = 2**40
BYTES_PER_GB = 2**30
TOTAL_ZONES = 256 # there are official 256 taxi zones

STRATEGIES = [ # partition, cluster
    ("No optimization", 0, 0),
    ("Cluster only", 0, 1),
    ("Partition only", 1, 0),
    ("Partition + Cluster", 1, 1),
]

# function
def load_booster(path: Path) -> xgb.Booster | None:
    if not path.exists():
        return None
    booster = xgb.Booster()
    booster.load_model(str(path))
    return booster

def build_row(booster, values: dict) -> pd.DataFrame:
    booster_features = booster.feature_names
    if booster_features and set(booster_features) == set(values.keys()):
        cols = list(booster_features)
    else:
        cols = FEATURES
    return pd.DataFrame([[values[c] for c in cols]], columns=cols)

def predict_bytes(booster, table_size_bytes: float, partition_ratio: float, cluster_ratio: float) -> pd.DataFrame:
    rows = []
    for name, has_part, has_clust in STRATEGIES:
        values = {
            "has_partition": has_part,
            "has_cluster": has_clust,
            "table_size_bytes": table_size_bytes,
            "partition_filter_ratio": partition_ratio,
            "cluster_filter_ratio": cluster_ratio
        }
        row = build_row(booster, values)
        pred = float(booster.predict(xgb.DMatrix(row)[0]))
        pred = min(max(pred, 0.0), table_size_bytes) # bounds for table_size
        rows.append({
            "strategy": name, "has_partition": has_part, 
            "has_cluster": has_clust, "predicted_bytes": pred
        })
    return pd.DataFrame(rows)

def add_cost_and_saving(df: pd.DataFrame, price_per_tib: float) -> pd.DataFrame:
    df = df.copy()
    df['cost'] = df['predicted_bytes'] / BYTES_PER_TIB * price_per_tib
    baseline_cost = df.loc[df.strategy == "No optimization", "cost"].iloc[0]
    df['saving_abs'] = baseline_cost - df['cost']
    df['saving_pct'] = np.where(baseline_cost > 0, df['saving_abs'] / baseline_cost * 100, 0.0)
    return df.sort_values('saving_abs').reset_index(drop=True)

def fetch_usd_idr_rate() -> float | None:
    try:
        resp = requests.get("https://api.frankfurter.app/latest?from=USD&to=IDR", timeout=5)
        resp.raise_for_status()
        return float(resp.json()['rates']['IDR'])
    except (requests.RequestException, KeyError, ValueError, TypeError):
        return None

def resolve_display_price(
        price_input: float, input_ccy: str, display_ccy: str, usd_idr_rate: float | None
) -> tuple[float, bool]:
    if input_ccy == display_ccy:
        return price_input, True
    if usd_idr_rate is None:
        return price_input, False
    if input_ccy == "USD" and display_ccy == "IDR":
        return price_input * usd_idr_rate, True
    if input_ccy == "IDR" and display_ccy == "USD":
        return price_input / usd_idr_rate, True
    return price_input, True

def format_money(amount: float, currency: str) -> str:
    if currency == "IDR":
        return f"Rp{amount:,.0f}"
    return f"${amount:,.4f}"

def format_bytes(n: float) -> str:
    if n >= 1e9:
        return f"{n / 1e9:,.2f} GB"
    return f"{n / 1e6:,.1f} MB"