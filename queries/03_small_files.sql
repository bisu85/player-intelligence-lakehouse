.timer on

-- Footer-only: count(*) is answered from metadata, no data pages read
SELECT count(*) FROM 's3://lakehouse/raw/events_sorted.parquet';
SELECT count(*) FROM 's3://lakehouse/raw/events_fragmented/**/*.parquet';

-- Full scan: actually reads data pages
SELECT event_type, count(*), sum(revenue_usd)
FROM 's3://lakehouse/raw/events_sorted.parquet' GROUP BY 1 ORDER BY 1;

SELECT event_type, count(*), sum(revenue_usd)
FROM 's3://lakehouse/raw/events_fragmented/**/*.parquet' GROUP BY 1 ORDER BY 1;