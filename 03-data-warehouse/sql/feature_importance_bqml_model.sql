SELECT
    feature,
    attribution / 1e6 AS attribution,
    ROUND(attribution / SUM(attribution) OVER () * 100, 2) AS pct_of_attribution
FROM
    ML.GLOBAL_EXPLAIN(MODEL `de-projects-beyond-zoomcamp.beyond_zoomcamp_module_03_dataset.xgb_bytes_predictor`)
ORDER BY attribution DESC;
