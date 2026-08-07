-- File-level metadata
SELECT num_rows, num_row_groups, format_version
FROM parquet_file_metadata('s3://lakehouse/raw/events_sorted.parquet');

-- Row-group / column-chunk detail: the footer statistics
SELECT row_group_id, path_in_schema, compression, num_values,
       total_compressed_size, stats_min, stats_max, stats_null_count
FROM parquet_metadata('s3://lakehouse/raw/events_sorted.parquet')
WHERE row_group_id < 2
ORDER BY row_group_id, path_in_schema;