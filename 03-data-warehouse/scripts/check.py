# scripts/check_zone_coverage.py — throwaway diagnostic, not part of the pipeline
from utils.common import TIERS, staging_month_bounds, tier_bounds
from utils.query_templates import zone_groups
from run_benchmark import cluster_row_counts

data_min, data_max = staging_month_bounds()

for tier in TIERS:
    if tier_bounds(tier, data_min, data_max) is None:
        continue
    zone_counts, total_rows = cluster_row_counts(tier)
    groups = zone_groups(zone_counts, total_rows)
    print(f"\ntier={tier}mo — {len(groups)} distinct ratio checkpoints reached (out of 9 targets):")
    for g in groups:
        print(f"  {len(g['zones']):>3} zones -> ratio={g['cluster_filter_ratio']:.4f}")