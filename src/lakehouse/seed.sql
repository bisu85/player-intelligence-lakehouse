-- Synthetic game telemetry matching the Stage 2 schema.
-- Grain: one row per event. 100k rows spanning ~180 days.
CREATE OR REPLACE TABLE events AS
SELECT
    md5(CONCAT(i::VARCHAR, '-', (i % 5000)::VARCHAR))          AS event_id,
    'P' || lpad(((i * 7919) % 5000)::VARCHAR, 6, '0')          AS player_id,
    TIMESTAMP '2026-01-01 00:00:00'
        + INTERVAL (i * 155) SECOND                            AS event_ts,
    CASE (i * 31) % 100
        WHEN 0 THEN 'purchase'
        ELSE CASE ((i * 31) % 5)
            WHEN 0 THEN 'session_start' WHEN 1 THEN 'session_end'
            WHEN 2 THEN 'level_complete' WHEN 3 THEN 'item_equip'
            ELSE 'ad_view' END
    END                                                        AS event_type,
    CASE WHEN (i * 31) % 100 = 0
         THEN ROUND((((i * 13) % 4999) / 100.0)::DECIMAL(10,2), 2)
         ELSE NULL END                                         AS revenue_usd
FROM range(100_000) t(i);