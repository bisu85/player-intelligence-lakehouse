from pyiceberg.transforms import DayTransform
from lakehouse.catalog import get_catalog

catalog = get_catalog()
table = catalog.load_table("game.events")

print("--- partition spec before ---")
print(table.spec())

with table.update_spec() as update:
    update.add_field("event_ts", DayTransform(), "event_day")

table.refresh()
print("--- partition spec after ---")
print(table.spec())
print(f"specs on record: {len(table.metadata.partition_specs)}")