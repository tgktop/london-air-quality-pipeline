# Source Documentation: https://duckdb.org/docs/data/json/overview.html
# Data Source: London Air Quality Network (LAQN) API (https://www.londonair.org.uk/Londonair/API/)

import duckdb

# Define database path
DB_PATH = "data/london_air.duckdb"

# Connect to DuckDB database
con = duckdb.connect(DB_PATH)

print("Transforming staging data into dim_sites...")

# Unnest 'Sites.Site' and safely handle empty coordinate strings using NULLIF
con.execute("""
    CREATE OR REPLACE TABLE dim_sites AS
    SELECT 
        site."@SiteCode" AS site_id,
        site."@SiteName" AS site_name,
        site."@LocalAuthorityName" AS borough_name,
        site."@SiteType" AS site_type,
        CAST(NULLIF(site."@Latitude", '') AS DOUBLE) AS latitude,
        CAST(NULLIF(site."@Longitude", '') AS DOUBLE) AS longitude,
        CURRENT_TIMESTAMP AS transformed_at
    FROM stg_raw_sites,
    UNNEST(Sites.Site) AS t(site);
""")

# Verify the row count of our new dimension table
site_count = con.execute("SELECT COUNT(*) FROM dim_sites").fetchone()[0]
print(f"Successfully transformed {site_count} monitoring sites into 'dim_sites'!")

# Preview the first 5 rows to verify the output
print("\nPreview of transformed sites:")
print(con.execute("SELECT site_id, site_name, borough_name, site_type, latitude, longitude FROM dim_sites LIMIT 5").fetchall())

con.close()
