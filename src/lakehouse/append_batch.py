import pyarrow.compute as pc
from lakehouse.catalog import get_catalog
from lakehouse.db import connect

catalog = get_catalog()
table = catalog.load_table("game.events")

before = len(table.scan().to_arrow())
print(f"rows before:     {before}")
print(f"snapshots before: {len(table.metadata.snapshots)}")

# A second batch: the shuffled file is the same 100k rows, so this doubles the table
con = connect()
arrow = con.sql(
    "SELECT * FROM 's3://lakehouse/raw/events_shuffled.parquet'"
).fetch_arrow_table()

table.append(arrow)
table.refresh()

print(f"rows after:      {len(table.scan().to_arrow())}")
print(f"snapshots after: {len(table.metadata.snapshots)}")
print(f"metadata now:    {table.metadata_location}")