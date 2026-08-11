from pyiceberg.types import StringType
from lakehouse.catalog import get_catalog

catalog = get_catalog()
table = catalog.load_table("game.events")

print("--- before ---")
print(table.schema())

with table.update_schema() as update:
    update.add_column("platform", StringType(), "ios / android / pc")
    update.rename_column("revenue_usd", "revenue")

table.refresh()
print("--- after ---")
print(table.schema())
print(f"metadata now: {table.metadata_location}")