import os
import duckdb
from dotenv import load_dotenv

load_dotenv()

def connect(database: str = ":memory:") -> duckdb.DuckDBPyConnection:
    """DuckDB connection with the local S3 endpoint configured."""
    con = duckdb.connect(database)
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute(
        """
        CREATE OR REPLACE SECRET minio (
            TYPE s3,
            KEY_ID  ?,
            SECRET  ?,
            ENDPOINT 'localhost:9000',
            URL_STYLE 'path',
            USE_SSL false,
            REGION 'us-east-1'
        );
        """,
        [os.environ["MINIO_ROOT_USER"], os.environ["MINIO_ROOT_PASSWORD"]],
    )
    return con