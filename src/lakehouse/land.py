from pathlib import Path
from lakehouse.db import connect

SEED_SQL = Path(__file__).parent / "seed.sql"

con = connect()
con.execute(SEED_SQL.read_text())

# Naturally time-sorted (event_ts increases with i) -> narrow min/max per row group
con.execute("""
    COPY events TO 's3://lakehouse/raw/events_sorted.parquet'
    (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 10_000);
""")

# Same rows, shuffled -> every row group spans the full range
con.execute("""
    COPY (SELECT * FROM events ORDER BY random())
    TO 's3://lakehouse/raw/events_shuffled.parquet'
    (FORMAT parquet, COMPRESSION zstd, ROW_GROUP_SIZE 10_000);
""")

print(con.sql("SELECT count(*) FROM 's3://lakehouse/raw/events_sorted.parquet'"))