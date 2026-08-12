from lakehouse.spark_session import get_spark

spark = get_spark()
spark.sql("SHOW NAMESPACES IN lk").show()
spark.sql("SHOW TABLES IN lk.game").show()
spark.sql("SELECT count(*) FROM lk.game.events").show()
spark.sql("""
    SELECT event_type, count(*) AS n, sum(revenue) AS rev
    FROM lk.game.events GROUP BY 1 ORDER BY 2 DESC
""").show()