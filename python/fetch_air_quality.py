"""
Data Extraction Script: London Air Quality Network (LAQN) API
- Connects to the Imperial College London ERG Air Quality API.
- Fetches metadata for monitoring sites across London and archives raw JSON snapshots locally.
- Ensures auditability and offline repeatability without hitting the API redundantly.
"""

import os
import requests
import json
from datetime import datetime

def fetch_laqn_sites():
    """
    Function to fetch baseline monitoring station metadata for London.
    Endpoint reference: https://api.erg.ic.ac.uk/AirQuality/help
    """
    # Base endpoint URL for monitoring sites filtered by the London group
    url = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=London/Json"
    
    print("Connecting to London Air Quality Network (LAQN) API...")
    
    try:
        # Send HTTP GET request to the API
        response = requests.get(url, timeout=10)
        
        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            data = response.json()
            
            # Ensure the raw data directory exists locally
            os.makedirs("data/raw", exist_ok=True)
            
            # Generate a clean timestamp string for the filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"data/raw/laqn_sites_{timestamp}.json"
            
            # Write the raw JSON response payload to disk (satisfies API courtesy & audit rules)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
                
            print(f"Success! Raw site metadata saved locally to {filepath}")
            return data
            
        else:
            print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during API connection: {e}")
        return None

if __name__ == "__main__":
    # Execute the extraction script when run directly from the terminal
    fetch_laqn_sites()

