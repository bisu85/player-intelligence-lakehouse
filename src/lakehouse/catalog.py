import os
from dotenv import load_dotenv
from pyiceberg.catalog.sql import SqlCatalog
from pyiceberg.catalog.rest import RestCatalog


load_dotenv()

WAREHOUSE = "s3://lakehouse/warehouse"

def get_catalog() -> SqlCatalog:
    return SqlCatalog(
        "local",
        **{
            "uri": os.environ["PG_URI"],
            "warehouse": WAREHOUSE,
            "s3.endpoint": "http://localhost:9000",
            "s3.access-key-id": os.environ["MINIO_ROOT_USER"],
            "s3.secret-access-key": os.environ["MINIO_ROOT_PASSWORD"],
            "s3.path-style-access": "true",
        },
    )

def get_rest_catalog() -> RestCatalog:
    return RestCatalog(
        "lakekeeper",
        **{
            "uri": "http://lakekeeper:8181/catalog",
            "warehouse": "lakehouse",
        },
    )