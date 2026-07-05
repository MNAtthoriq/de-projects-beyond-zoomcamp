from datetime import datetime, timedelta
from utils.common import PARTITION_COL, CLUSTER_COL

DATE_SPANS_DAYS = [1, 7, 15, 30, 45, 60, 90, 120, 150, 180, 210, 250, 300, 360] # not use 365 because _month_end_date() uses 28th as anchor point 
WINDOW_OFFSETS_DAYS = [0, 45, 120]

SAMPLE_CLUSTERS = [237, 229, 152, 254, 54, 99, 187]  # PULocationID - based on percentile of cluster row counts for 12mo tier

def _month_end_date(ym: str) -> str:
    # every month has at least 28 days, good enough for a window anchor point
    return f"{ym}-28"

def _month_start_date(ym: str) -> str:
    return f"{ym}-01"

def _date_windows(tier_start_month: str, tier_end_month: str):
    tier_start_str = _month_start_date(tier_start_month)
    tier_end_str = _month_end_date(tier_end_month)
    tier_start = datetime.fromisoformat(tier_start_str)
    tier_end = datetime.fromisoformat(tier_end_str)

    total_days = (tier_end - tier_start).days

    for span in DATE_SPANS_DAYS:
        for offset in WINDOW_OFFSETS_DAYS:
            window_start = tier_end - timedelta(days=offset + span)
            if window_start < tier_start:
                break

            yield {
                "start_expr": f"DATE_SUB('{tier_end_str}', INTERVAL {offset + span} DAY)",
                "end_expr": f"DATE_SUB('{tier_end_str}', INTERVAL {offset} DAY)",
                "filter_days": span,
                "total_days": total_days
            }

def build_query_matrix(tier_start_month: str, tier_end_month: str):
    queries = []
    qid = 0

    for window in _date_windows(tier_start_month, tier_end_month):
        date_partition = f"DATE({PARTITION_COL}) >= {window['start_expr']} AND DATE({PARTITION_COL}) < {window['end_expr']}"
        add_info = {"partition_filter_ratio": window["filter_days"]/window["total_days"] if window["total_days"] > 0 else 0}

        for zone in SAMPLE_CLUSTERS:
            qid += 1
            queries.append(
                {
                    "query_id": qid,
                    "sql_template": f"SELECT COUNT(*) AS n FROM {{table}} WHERE {date_partition} AND {CLUSTER_COL} = {zone}",
                    "zone": zone,
                    **add_info
                }
            )

    return queries