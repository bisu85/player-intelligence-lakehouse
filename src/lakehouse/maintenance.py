"""Iceberg table maintenance. Order matters: compact -> expire -> orphans."""
import trino

TABLE = "iceberg.game.events"

def run(sql: str, conn):
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def main():
    conn = trino.dbapi.connect(host="localhost", port=8090, user="maintenance")

    before = run(f'SELECT count(*), sum(file_size_in_bytes) FROM iceberg.game."events$files"', conn)
    print(f"before: {before}")

    # 1. compact — only files under the threshold
    run(f"ALTER TABLE {TABLE} EXECUTE optimize(file_size_threshold => '100MB')", conn)

    # 2. expire snapshots — frees files the compaction superseded
    run(f"ALTER TABLE {TABLE} EXECUTE expire_snapshots(retention_threshold => '7d')", conn)

    # 3. orphans — NEVER below the default retention in production
    run(f"ALTER TABLE {TABLE} EXECUTE remove_orphan_files(retention_threshold => '7d')", conn)

    after = run(f'SELECT count(*), sum(file_size_in_bytes) FROM iceberg.game."events$files"', conn)
    print(f"after: {after}")

if __name__ == "__main__":
    main()