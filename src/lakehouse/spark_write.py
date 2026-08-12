from lakehouse.spark_session import get_spark

spark = get_spark()

before = spark.sql("SELECT count(*) AS n FROM lk.game.events").collect()[0]["n"]
print(f"before: {before}")

spark.sql("""
    INSERT INTO lk.game.events
    SELECT * FROM lk.game.events WHERE event_type = 'purchase' LIMIT 100
""")

after = spark.sql("SELECT count(*) AS n FROM lk.game.events").collect()[0]["n"]
print(f"after:  {after}")

spark.sql("SELECT * FROM lk.game.events.snapshots ORDER BY committed_at").show(truncate=False)
spark.sql("SELECT * FROM lk.game.events.files LIMIT 5").show(truncate=False)