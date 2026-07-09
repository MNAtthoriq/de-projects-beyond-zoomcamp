CREATE OR REPLACE MODEL `de-projects-beyond-zoomcamp.beyond_zoomcamp_module_03_dataset.xgb_bytes_predictor`
OPTIONS(
    MODEL_TYPE              = 'BOOSTED_TREE_REGRESSOR',
    INPUT_LABEL_COLS        = ['bytes_processed'],
    BOOSTER_TYPE            = 'GBTREE',
    TREE_METHOD             = 'AUTO',
    MAX_TREE_DEPTH          = 6,
    MIN_TREE_CHILD_WEIGHT   = 1,
    LEARN_RATE              = 0.300000012,
    MAX_ITERATIONS          = 100,
    NUM_PARALLEL_TREE       = 1,
    SUBSAMPLE               = 1.0,
    COLSAMPLE_BYTREE        = 1.0,
    COLSAMPLE_BYLEVEL       = 1.0,
    COLSAMPLE_BYNODE        = 1.0,
    L1_REG                  = 0.0,
    L2_REG                  = 1.0,
    MIN_SPLIT_LOSS          = 0.0,
    DATA_SPLIT_METHOD       = 'CUSTOM',
    DATA_SPLIT_COL          = 'is_test',
    EARLY_STOP              = FALSE,
    ENABLE_GLOBAL_EXPLAIN   = TRUE
) AS
SELECT
    has_partition,
    has_cluster,
    table_size_bytes,
    partition_filter_ratio,
    cluster_filter_ratio,
    bytes_processed,
    MOD(ABS(FARM_FINGERPRINT(CONCAT(CAST(tier_months AS STRING), '|', variant, '|', CAST(query_id AS STRING)))), 10) < 2 AS is_test
FROM `de-projects-beyond-zoomcamp.beyond_zoomcamp_module_03_dataset.benchmark_results`;
