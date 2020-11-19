import os

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "api_db")
POSTGRES_DBNAME = os.environ.get("POSTGRES_DB", "mermaid")
POSTGRES_SCHEMA = os.environ.get("POSTGRES_SCHEMA", "public")
POSTGRES_PORT = int(os.environ.get("POSTGRES_PORT", 5432))
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASS = os.environ.get("POSTGRES_PASS", "postgres")

POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"

COUCHDB_URL = os.environ.get("COUCHDB_URL", "http://admin:password@localhost:5984/")
COUCHDB_DBNAME = os.environ.get("COUCHDB_DBNAME", "mermaid")
