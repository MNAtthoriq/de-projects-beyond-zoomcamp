WITH evals AS (
    SELECT 
        'test' AS dataset, 
        r2_score, 
        mean_absolute_error / 1e6 AS mean_absolute_error
    FROM ML.EVALUATE(MODEL `de-projects-beyond-zoomcamp.beyond_zoomcamp_module_03_dataset.xgb_bytes_predictor`)
    UNION ALL
    SELECT 
        'train' AS dataset, 
        r2_score, 
        mean_absolute_error / 1e6 AS mean_absolute_error
    FROM ML.EVALUATE(MODEL `de-projects-beyond-zoomcamp.beyond_zoomcamp_module_03_dataset.xgb_bytes_predictor`, (
        SELECT
            has_partition,
            has_cluster,
            table_size_bytes,
            partition_filter_ratio,
            cluster_filter_ratio,
            bytes_processed
        FROM `de-projects-beyond-zoomcamp.beyond_zoomcamp_module_03_dataset.benchmark_results`
        WHERE NOT (MOD(ABS(FARM_FINGERPRINT(CONCAT(CAST(tier_months AS STRING), '|', variant, '|', CAST(query_id AS STRING)))), 10) < 2)
))),

pivoted AS (
    SELECT
        MAX(IF(dataset = 'train', r2_score, NULL))              AS r2_train,
        MAX(IF(dataset = 'test', r2_score, NULL))               AS r2_test,
        MAX(IF(dataset = 'train', mean_absolute_error, NULL))   AS mae_train_mb,
        MAX(IF(dataset = 'test', mean_absolute_error, NULL))    AS mae_test_mb
    FROM evals
)

SELECT
    ROUND(r2_train, 4)                                              AS r2_train,
    ROUND(r2_test, 4)                                               AS r2_test,
    ROUND(ABS(r2_train - r2_test) / ABS(r2_train) * 100, 4)         AS r2_gap_pct,
    ROUND(mae_train_mb, 4)                                          AS mae_train_mb,
    ROUND(mae_test_mb, 4)                                           AS mae_test_mb,
    ROUND(ABS(mae_train_mb - mae_test_mb) / mae_train_mb * 100, 4)  AS mae_gap_pct,
    CASE
        WHEN r2_train < 0.90 THEN 'underfit'
        WHEN ABS(r2_train - r2_test) / ABS(r2_train) * 100 > 10 THEN 'overfit'
        ELSE 'good fit'
    END                                                             AS fit
FROM pivoted;
