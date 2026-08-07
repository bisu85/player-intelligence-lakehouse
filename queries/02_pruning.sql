-- Total row groups vs. row groups a WHERE event_ts > '2026-05-01' must actually read
SELECT
    'sorted' AS layout,
    count(*) AS total_row_groups,
    count(*) FILTER (WHERE stats_max::TIMESTAMP > TIMESTAMP '2026-05-01') AS must_read
FROM parquet_metadata('s3://lakehouse/raw/events_sorted.parquet')
WHERE path_in_schema = 'event_ts'

UNION ALL

SELECT
    'shuffled',
    count(*),
    count(*) FILTER (WHERE stats_max::TIMESTAMP > TIMESTAMP '2026-05-01')
FROM parquet_metadata('s3://lakehouse/raw/events_shuffled.parquet')
WHERE path_in_schema = 'event_ts';