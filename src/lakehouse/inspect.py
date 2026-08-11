# src/lakehouse/inspect.py
from lakehouse.catalog import get_catalog

table = get_catalog().load_table("game.events")

print(f"metadata:  {table.metadata_location}")
print(f"snapshots: {len(table.metadata.snapshots)}")
print(f"rows:      {len(table.scan().to_arrow())}")
print()
print(table.schema())
print()
print(table.scan(selected_fields=("player_id", "revenue", "platform")).to_arrow().slice(0, 5))