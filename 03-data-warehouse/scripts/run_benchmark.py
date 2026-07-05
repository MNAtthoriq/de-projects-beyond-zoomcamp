"""
Run a benchmark to compare the performance of different table variants
"""
import csv
from pathlib import Path
from google.cloud import bigquery
from tqdm import tqdm
from utils.common import (
    CLUSTER_COL, TIERS, VARIANTS, client, 
    staging_month_bounds, table_fqn, tier_bounds
)
from utils.query_templates import build_query_matrix

def dry_run_bytes(sql: str) -> int:
    """Perform a dry-run of a SQL query and return the number of bytes processed"""
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    job = client.query(sql, job_config=job_config)
    return job.total_bytes_processed

def cluster_row_counts(tier: int):
    """Get the row counts for each cluster zone in a given tier's clust variant table"""
    fqn = table_fqn(tier, "clust")
    sql = f"SELECT {CLUSTER_COL} AS zone, COUNT(*) AS n FROM `{fqn}` GROUP BY {CLUSTER_COL}"
    rows = list(client.query(sql).result())
    counts = {row.zone: row.n for row in rows}
    return counts, sum(counts.values())

def main():
    """Run the benchmark for all tier and variant combinations, writing results to a CSV file"""
    data_min, data_max = staging_month_bounds()
    
    plan = []
    for tier in TIERS:
        bounds = tier_bounds(tier, data_min, data_max)
        if bounds is None:
            print(f"  skipping {tier}mo tier - not enough history yet ({data_min}..{data_max})")
            continue
        start_month, end_month = bounds
        queries = build_query_matrix(start_month, end_month)

        print(f"[{tier}mo] cluster_filter_ratio lookup (1 real query)...")
        zone_counts, total_rows = cluster_row_counts(tier)

        for variant in VARIANTS:
            fqn = table_fqn(tier, variant)
            table_size_bytes = client.get_table(fqn).num_bytes
            for q in queries:
                plan.append((tier, variant, q, fqn, zone_counts, total_rows, table_size_bytes))
    
    print(f"Total (tier, variant, query) combinations: {len(plan)}")

    results = []
    failed = 0
    for tier, variant, q, fqn, zone_counts, total_rows, table_size_bytes in tqdm(plan, desc="dry-run queries"):
        sql = q["sql_template"].format(table=fqn)
        try:
            bytes_processed = dry_run_bytes(sql)
        except Exception as e:
            failed += 1
            tqdm.write(f"  dry_run failed (tier={tier}mo, variant={variant}, query_id={q['query_id']}): {e}")
            continue
        
        results.append(
            {
                "tier_months": tier,
                "variant": variant,
                "query_id": q["query_id"],
                "has_partition": variant in ("part", "partclust"),
                "has_cluster": variant in ("clust", "partclust"),
                "table_size_bytes": table_size_bytes,
                "partition_filter_ratio": q["partition_filter_ratio"],
                "cluster_filter_ratio": zone_counts.get(q["zone"], 0) / total_rows if total_rows > 0 else 0,
                "bytes_processed": bytes_processed
            }
        )
    
    results_dir = (Path(__file__).resolve().parent / ".." / "results").resolve()
    results_dir.mkdir(parents=True, exist_ok=True)
    out_path = results_dir / "benchmark_results.csv"
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
 
    print(f"\nWrote {len(results)} rows to {out_path}")

if __name__ == "__main__":
    main()