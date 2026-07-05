"""
Common utility functions for data warehouse scripts
"""
from pathlib import Path
from dotenv import load_dotenv
import os
from google.cloud import bigquery

# load .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# google cloud variables
PROJECT = os.environ["GCP_PROJECT_ID"]
DATASET = os.environ["GCP_DATASET"]
BUCKET = os.environ["GCP_GCS_BUCKET"]
STAGING_TABLE = f"{PROJECT}.{DATASET}.trips_staging"

# table variables
TIERS = [2, 4, 6, 8, 10, 12] # months
VARIANTS = ["none", "part", "clust", "partclust"]
PARTITION_COL = "pickup_datetime"
CLUSTER_COL = "PULocationID"

# init bigquery client
client = bigquery.Client(project=PROJECT)

def shift_month(ym: str, delta: int) -> str:
    """Shift a YYYY-MM string by delta months, returning a YYYY-MM string"""
    y, m = int(ym[:4]), int(ym[5:7])
    total = y * 12 + (m - 1) + delta # m-1 because we want use 0-based month for calculation
    y, m = divmod(total, 12)
    return f"{y:04d}-{m + 1:02d}" # m+1 because we want to return 1-based month

def staging_month_bounds():
    """Get the minimum and maximum months in the staging table"""
    query = f"""
    SELECT
        MIN(source_month) AS min_m,
        MAX(source_month) AS max_m
    FROM `{STAGING_TABLE}`
    """
    row = next(iter(client.query(query).result()))
    return row.min_m, row.max_m

def tier_bounds(tier_months: int, data_min_month: str, data_max_month: str):
    """Get the start and end months for a given tier, or None if not enough history"""
    start = shift_month(data_max_month, -(tier_months - 1))
    if start < data_min_month:
        return None
    return start, data_max_month

def table_name(tier_months: int, variant: str) -> str:
    """Get table name for a given tier and variant"""
    return f"trips_{tier_months}mo_{variant}"

def table_fqn(tier_months: int, variant: str) -> str:
    """Get fully qualified table name for a given tier and variant"""
    return f"{PROJECT}.{DATASET}.{table_name(tier_months, variant)}"