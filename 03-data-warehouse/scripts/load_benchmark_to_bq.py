"""
Load benchmark_results.csv into table in BigQuery
"""
import pandas as pd
from pathlib import Path
from google.cloud import bigquery
from utils.common import (
    PROJECT, DATASET, BUCKET, client
)

# path and schema
df_path = Path.cwd() / ".." / "results" / "benchmark_results.csv"
TABLE = f"{PROJECT}.{DATASET}.benchmark_results"
SCHEMA = [
    bigquery.SchemaField("tier_months", "INTEGER"),
    bigquery.SchemaField("variant", "STRING"),
    bigquery.SchemaField("query_id", "INTEGER"),
    bigquery.SchemaField("has_partition", "INTEGER"),
    bigquery.SchemaField("has_cluster", "INTEGER"),
    bigquery.SchemaField("table_size_bytes", "INTEGER"),
    bigquery.SchemaField("partition_filter_ratio", "FLOAT"),
    bigquery.SchemaField("cluster_filter_ratio", "FLOAT"),
    bigquery.SchemaField("bytes_processed", "INTEGER"),
]

def main():
    # read data
    df = pd.read_csv(df_path)
    # change bool into int
    df['has_partition'] = df['has_partition'].astype(int)
    df['has_cluster'] = df['has_cluster'].astype(int)

    # load to bq
    job_config = bigquery.LoadJobConfig(schema=SCHEMA, write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(df, TABLE, job_config=job_config)
    job.result()

    # validate result
    table = client.get_table(TABLE)
    has_partition_type = next(f.field_type for f in table.schema if f.name == "has_partition")
    print(f"Loaded {table.num_rows:,} rows into {TABLE}")
    print(f"has_partition column type: {has_partition_type} (should be INTEGER, not BOOLEAN)")

if __name__ == "__main__":
    main()