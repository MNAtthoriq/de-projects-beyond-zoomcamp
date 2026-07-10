"""
Query templates for generating SQL queries for different time windows and cluster zones
"""
from datetime import datetime, timedelta
from utils.common import PARTITION_COL, CLUSTER_COL

# combination variable for partition column
PARTITION_RATIO_TARGETS = [
    0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15, 0.2, 0.3,
    0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0
]
OFFSET_RATIO_TARGETS = [0.0, 0.15, 0.3, 0.5]
# combination variable for cluster column
CLUSTER_RATIO_TARGETS = [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 1.0]

def _month_start_date(ym: str) -> str:
    """Get the start date of a month given a YYYY-MM string"""
    return f"{ym}-01"

def _month_end_date(ym: str) -> str:
    """Get the end date of a month given a YYYY-MM string"""
    # every month has at least 28 days, good enough for a window anchor point
    return f"{ym}-28"

def _date_windows(tier_start_month: str, tier_end_month: str):
    """Generate date windows for a given tier's start and end months"""
    tier_start_str = _month_start_date(tier_start_month)
    tier_end_str = _month_end_date(tier_end_month)
    tier_start = datetime.fromisoformat(tier_start_str)
    tier_end = datetime.fromisoformat(tier_end_str)

    # calculate total days in the tier range
    total_days = (tier_end - tier_start).days
    if total_days <= 0:
        raise ValueError("Total days between start and end month must larger than 0")

    seen = set() 
    for span_ratio in PARTITION_RATIO_TARGETS: 
        span = max(1, min(total_days, round(span_ratio * total_days)))
        for offset_ratio in OFFSET_RATIO_TARGETS:
            offset = round(offset_ratio * total_days)
            window_start = tier_end - timedelta(days=offset + span)
            if window_start < tier_start: # if outside history range, skip
                break
            
            key = (span, offset)
            if key in seen:
                continue
            seen.add(key)

            yield {
                "start_expr": f"DATE_SUB('{tier_end_str}', INTERVAL {offset + span} DAY)",
                "end_expr": f"DATE_SUB('{tier_end_str}', INTERVAL {offset} DAY)",
                "filter_days": span,
                "total_days": total_days
            }

def zone_groups(zone_counts: dict, total_rows: int):
    """Generate cumulative zone groups greedily"""
    if total_rows <= 0 or not zone_counts:
        return []
    
    ranked = sorted(zone_counts.items(), key=lambda kv: kv[1], reverse=True)
    groups = []
    cum_rows, cum_zones = 0, []
    target_idx = 0
    for zone, count in ranked:
        cum_rows += count
        cum_zones.append(zone)
        ratio = cum_rows / total_rows if total_rows else 0
        if target_idx < len(CLUSTER_RATIO_TARGETS) and ratio >= CLUSTER_RATIO_TARGETS[target_idx]:
            groups.append({"zones": list(cum_zones), "cluster_filter_ratio": ratio})
            while target_idx < len(CLUSTER_RATIO_TARGETS) and ratio >= CLUSTER_RATIO_TARGETS[target_idx]:
                target_idx += 1
        if target_idx >= len(CLUSTER_RATIO_TARGETS):
            break
    return groups

def build_query_matrix(tier_start_month: str, tier_end_month: str, zone_counts: dict, total_rows: int):
    """Build a matrix of queries for different date windows and cluster zones"""
    queries = []
    qid = 0

    for window in _date_windows(tier_start_month, tier_end_month):
        date_partition = f"DATE({PARTITION_COL}) >= {window['start_expr']} AND DATE({PARTITION_COL}) < {window['end_expr']}"
        partition_filter_ratio = window["filter_days"] / window["total_days"] if window["total_days"] > 0 else 0

        for group in zone_groups(zone_counts, total_rows):
            qid += 1
            zone_list = ", ".join(str(z) for z in group["zones"])
            # only one type of query because we already processed different table variants (none, part, clust, partclust) 
            queries.append(
                {
                    "query_id": qid,
                    "sql_template": f"SELECT COUNT(*) AS n FROM {{table}} WHERE {date_partition} AND {CLUSTER_COL} IN ({zone_list})",
                    "partition_filter_ratio": partition_filter_ratio,
                    "cluster_filter_ratio": group["cluster_filter_ratio"]
                }
            )

    return queries