"""
Build table variants for different time windows and cluster zones
"""
import csv
from google.cloud import bigquery
from utils.common import (
    BUCKET, STAGING_TABLE, client,
    TIERS, VARIANTS, PARTITION_COL, CLUSTER_COL,
    staging_month_bounds, tier_bounds, table_name, table_fqn
)
from pathlib import Path

def load_staging_table():
    """Load raw parquet files from GCS into the staging table in BigQuery"""
    print(f"Loading raw parquet -> {STAGING_TABLE}")
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    uris = [
        f"gs://{BUCKET}/raw/yellow/*.parquet",
        f"gs://{BUCKET}/raw/green/*.parquet"
    ]
    job = client.load_table_from_uri(uris, STAGING_TABLE, job_config=job_config)
    job.result()
    table = client.get_table(STAGING_TABLE)
    print(f"  loaded {table.num_rows:,} rows, {table.num_bytes / 1e9:.2f} GB")

def variant_ddl(fqn: str, variant: str, where_clause: str) -> str:
    """Generate DDL for creating a table variant based on the staging table"""
    select = f"SELECT * FROM `{STAGING_TABLE}` WHERE {where_clause}"
    target = f"`{fqn}`"

    if variant == "none":
        return f"CREATE OR REPLACE TABLE {target} AS {select}"
    if variant == "part":
        return f"CREATE OR REPLACE TABLE {target} PARTITION BY DATE({PARTITION_COL}) AS {select}"
    if variant == "clust":
        return f"CREATE OR REPLACE TABLE {target} CLUSTER BY {CLUSTER_COL} AS {select}"
    if variant == "partclust":
        return f"CREATE OR REPLACE TABLE {target} PARTITION BY DATE({PARTITION_COL}) CLUSTER BY {CLUSTER_COL} AS {select}"
    raise ValueError(variant)

def build_tiers():
    """Build table variants for each tier and variant, returning a manifest of created tables"""
    data_min, data_max = staging_month_bounds()
    print(f"Data spans from {data_min} to {data_max}")

    manifest = [] # manifest for sanity check of created tables
    for tier in TIERS:
        bounds = tier_bounds(tier, data_min, data_max)
        if bounds is None:
            print(f"  skipping {tier}mo tier - not enough history yet ({data_min}..{data_max})")
            continue
        start_month, end_month = bounds
        where_clause = f"source_month BETWEEN '{start_month}' AND '{end_month}'"

        for variant in VARIANTS:
            fqn = table_fqn(tier, variant)
            name = table_name(tier, variant)
            print(f"Building {name} ({start_month}..{end_month})...")
            client.query(f"DROP TABLE IF EXISTS `{fqn}`").result()
            client.query(variant_ddl(fqn, variant, where_clause)).result()

            table = client.get_table(fqn)
            manifest.append(
                {
                    "table_name": name,
                    "tier_months": tier,
                    "variant": variant,
                    "has_partition": variant in ("part", "partclust"),
                    "has_cluster": variant in ("clust", "partclust"),
                    "start_month": start_month,
                    "end_month": end_month,
                    "num_rows": table.num_rows,
                    "size_bytes": table.num_bytes,
                    "size_gb": round(table.num_bytes / 1e9, 4),
                }
            )
            print(f"  {table.num_rows:,} rows, {table.num_bytes / 1e9:.3f} GB")
    return manifest

if __name__ == "__main__":
    load_staging_table()
    manifest = build_tiers()

    results_dir = (Path(__file__).resolve().parent / ".." / "results").resolve()
    results_dir.mkdir(exist_ok=True)

    if manifest: # manifest for sanity check
        manifest_file = results_dir / "table_manifest.csv"

        with manifest_file.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=manifest[0].keys())
            writer.writeheader()
            writer.writerows(manifest)

        print(f"\nWrote manifest for {len(manifest)} tables to {manifest_file}")
    else:
        print("No tables were created.")