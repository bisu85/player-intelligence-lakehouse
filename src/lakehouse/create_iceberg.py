import pyarrow.parquet as pq
from lakehouse.catalog import get_catalog
from lakehouse.db import connect

catalog = get_catalog()
catalog.create_namespace_if_not_exists("game")

# Pull yesterday's Parquet into memory as an Arrow table
con = connect()
arrow = con.sql("SELECT * FROM 's3://lakehouse/raw/events_sorted.parquet'").fetch_arrow_table()
print(f"source rows: {arrow.num_rows}")

table = catalog.create_table_if_not_exists("game.events", schema=arrow.schema)
table.append(arrow)

print(f"table rows:  {len(table.scan().to_arrow())}")
print(f"metadata:    {table.metadata_location}")