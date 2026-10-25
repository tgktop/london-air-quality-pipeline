import duckdb

def export_sites_to_json():
    # Connect to your DuckDB database
    conn = duckdb.connect("data/london_air.duckdb")
    
    # Export the dim_sites table directly to the app/ directory as JSON
    query = """
    COPY (
        SELECT site_id, site_name, latitude, longitude, site_type, borough_name 
        FROM dim_sites
    ) TO 'app/sites.json' (FORMAT JSON, ARRAY TRUE);
    """
    
    conn.execute(query)
    conn.close()
    print("Successfully exported dim_sites to app/sites.json!")

if __name__ == "__main__":
    export_sites_to_json()
