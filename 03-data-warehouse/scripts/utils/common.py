from pathlib import Path
from dotenv import load_dotenv
import os
from google.cloud import bigquery

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

PROJECT = os.environ["GCP_PROJECT_ID"]
DATASET = os.environ["GCP_DATASET"]
BUCKET = os.environ["GCP_GCS_BUCKET"]

STAGING_TABLE = f"{PROJECT}.{DATASET}.trips_staging"

TIERS = [2, 4, 6, 8, 10, 12]
VARIANTS = ["none", "part", "clust", "partclust"]
PARTITION_COL = "pickup_datetime"
CLUSTER_COL = "PULocationID"


client = bigquery.Client(project=PROJECT)

def shift_month(ym: str, delta: int) -> str:
    y, m = int(ym[:4]), int(ym[5:7])
    total = y * 12 + (m - 1) + delta
    y, m = divmod(total, 12)
    return f"{y:04d}-{m + 1:02d}"

def staging_month_bounds():
    query = f"""
    SELECT
        MIN(source_month) AS min_m,
        MAX(source_month) AS max_m
    FROM `{STAGING_TABLE}`
    """
    row = next(iter(client.query(query).result()))
    return row.min_m, row.max_m

def tier_bounds(tier_months: int, data_min_month: str, data_max_month: str):
    start = shift_month(data_max_month, -(tier_months - 1))
    if start < data_min_month:
        return None
    return start, data_max_month

def table_name(tier_months: int, variant: str) -> str:
    return f"trips_{tier_months}mo_{variant}"

def table_fqn(tier_months: int, variant: str) -> str:
    return f"{PROJECT}.{DATASET}.{table_name(tier_months, variant)}"