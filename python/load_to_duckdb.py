# Source Documentation: https://duckdb.org/docs/data/json/overview.html
# Data Source: London Air Quality Network (LAQN) API (https://www.londonair.org.uk/Londonair/API/)

import glob
import os
import duckdb

# Define paths
RAW_DIR = "data/raw"
DB_PATH = "data/london_air.duckdb"

# Connect to (or create) DuckDB database
con = duckdb.connect(DB_PATH)

print("Connecting to DuckDB...")

# Find the latest raw JSON snapshot
json_files = glob.glob(f"{RAW_DIR}/laqn_sites_*.json")
if not json_files:
    raise FileNotFoundError("No raw JSON files found in data/raw/")

latest_file = max(json_files, key=os.path.getctime)
print(f"Ingesting latest snapshot: {latest_file}")

# Load raw JSON directly into an operational staging table using DuckDB's native JSON extension
con.execute(f"""
    CREATE TABLE IF NOT EXISTS stg_raw_sites AS 
    SELECT * FROM read_json_auto('{latest_file}');
""")

# Count total ingested monitoring sites
site_count = con.execute("SELECT COUNT(*) FROM stg_raw_sites").fetchone()[0]
print(f"Successfully ingested {site_count} sites into DuckDB 'stg_raw_sites' table!")

con.close()
