from lakehouse.catalog import get_catalog, get_rest_catalog

old = get_catalog()          # Postgres SqlCatalog
new = get_rest_catalog()     # Lakekeeper REST

table = old.load_table("game.events")
metadata_location = table.metadata_location
print(f"existing metadata: {metadata_location}")

new.create_namespace_if_not_exists("game")
new.register_table("game.events", metadata_location)

registered = new.load_table("game.events")
print(f"rows via Lakekeeper: {len(registered.scan().to_arrow())}")
print(f"snapshots:           {len(registered.metadata.snapshots)}")