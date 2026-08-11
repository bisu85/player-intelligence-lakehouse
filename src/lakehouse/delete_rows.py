from lakehouse.catalog import get_catalog

catalog = get_catalog()
table = catalog.load_table("game.events")

before = len(table.scan().to_arrow())
files_before = len(list(table.scan().plan_files()))
print(f"rows: {before}, data files: {files_before}")

table.delete(delete_filter="player_id = 'P000042'")
table.refresh()

after = len(table.scan().to_arrow())
files_after = len(list(table.scan().plan_files()))
print(f"rows: {after}, data files: {files_after}")
print(f"deleted: {before - after}")
print(f"snapshots: {len(table.metadata.snapshots)}")