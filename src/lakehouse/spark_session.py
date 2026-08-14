import os
from dotenv import load_dotenv
from pyspark.sql import SparkSession

load_dotenv()

ICEBERG_VERSION = "1.11.0"
PACKAGES = ",".join([
    f"org.apache.iceberg:iceberg-spark-runtime-4.0_2.13:{ICEBERG_VERSION}",
    f"org.apache.iceberg:iceberg-aws-bundle:{ICEBERG_VERSION}",
])

def get_spark(app_name: str = "lakehouse") -> SparkSession:
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[2]")
        .config("spark.jars.packages", PACKAGES)
        .config("spark.sql.extensions",
                "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        # register a catalog named "lk"
        .config("spark.sql.catalog.lk", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.lk.type", "rest")
        .config("spark.sql.catalog.lk.uri", "http://lakekeeper:8181/catalog")
        .config("spark.sql.catalog.lk.warehouse", "lakehouse")
        .config("spark.sql.catalog.lk.io-impl", "org.apache.iceberg.aws.s3.S3FileIO")
        .config("spark.sql.catalog.lk.s3.endpoint", "http://localhost:9000")
        .config("spark.sql.catalog.lk.s3.path-style-access", "true")
        .config("spark.sql.catalog.lk.s3.access-key-id", os.environ["MINIO_ROOT_USER"])
        .config("spark.sql.catalog.lk.s3.secret-access-key", os.environ["MINIO_ROOT_PASSWORD"])
        .config("spark.driver.memory", "2g")
        .getOrCreate()
    )