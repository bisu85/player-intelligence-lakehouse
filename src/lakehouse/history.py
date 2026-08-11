from lakehouse.catalog import get_catalog

table = get_catalog().load_table("game.events")

for snap in table.metadata.snapshots:
    print(f"{snap.snapshot_id}  {snap.timestamp_ms}  {snap.summary.operation}")

print(f"\ncurrent: {table.metadata.current_snapshot_id}")

first = table.metadata.snapshots[0].snapshot_id
#table.manage_snapshots().rollback_to_snapshot(first).commit()

print(f"rows now:            {len(table.scan().to_arrow())}")
print(f"rows at snapshot 1:  {len(table.scan(snapshot_id=first).to_arrow())}")