# CleanAir London Intelligence Hub

An automated, serverless ELT pipeline and decision-first web application designed to transform fragmented London Air Quality Network (LAQN) telemetry into actionable spatial intelligence for urban planners and local council leaders.

---

## What I built and who for

### Who It Is For
* **Primary Audience (Non-Technical):** Urban planners, local council leaders, environmental policy advisors, and public health officers who require immediate spatial clarity and decision-ready numbers—not raw spreadsheets, complex SQL queries, or Python scripts.
* **Secondary Audience (Technical):** Data engineers and IT leads evaluating whether the pipeline architecture is lightweight, reliable, scalable, and compliant with API usage terms.

### What Was Built
* **Modular ELT Pipeline:** A Python-based extraction and transformation workflow paired with DuckDB for local analytical storage and automated deduplication.
* **Serverless Architecture:** A zero-cost architecture that exports clean analytics to static JSON datasets, completely eliminating the need for paid cloud servers or active database hosting.
* **Decision-First Web Application:** An interactive single-page dashboard featuring an Executive Policy Summary Box, key exposure metrics (such as the 49.2% Roadside Exposure Share), a borough-wide geospatial map, and a station directory for ground-level enforcement.

---

## The data

* **Source:** London Air Quality Network (LAQN) API hosted by the Environmental Research Group at Imperial College London.
* **Structure:** Ingests complex, multi-endpoint nested JSON payloads covering monitoring site classifications, geographic coordinates, and time-series pollutant telemetry (NO2, PM2.5, PM10).
* **API Courtesy & Storage:** All fetched and transformed data is cached and stored locally in DuckDB (`data/london_air.duckdb`) to avoid redundant requests, adhering strictly to API usage rules and fair-use guidelines.

---

## How it works

1. **Extract (`python/fetch_air_quality.py`):** Queries the LAQN API endpoints to fetch monitoring site metadata and raw pollutant readings.
2. **Transform & Model (`python/transform_air_quality_data.py`):** Cleans, flattens, and standardizes nested JSON payloads. Handles missing values, standardizes borough names, and structures tables for analytical performance.
3. **Load & Deduplicate (`python/load_to_duckdb.py`):** Ingests structured telemetry into `data/london_air.duckdb`. Operates incrementally—appending only new telemetry records on each run while enforcing primary key constraints to eliminate duplicates.
4. **Export (`python/export_to_web.py`):** Generates static JSON files (`app/sites.json`) containing pre-aggregated metrics for instant UI consumption.
5. **Serve (`app/index.html`):** Renders the frontend interface using standard HTML/CSS/JavaScript and Leaflet maps, fetching static data with zero database query latency.

---

## How to run it

This project is configured to run in a **Linux Terminal (e.g., ChromeOS Crostini / Debian)** using Python 3 and a local HTTP server.

### Prerequisites & Dependencies
Open your Linux terminal and install the required Python packages:
pip3 install duckdb requests

### Step 1: Clone the Repository
git clone [https://github.com/tgktop/london-air-quality-pipeline.git](https://github.com/tgktop/london-air-quality-pipeline.git)
cd london-air-quality-pipeline

### Step 2: Execute the Pipeline
Run the modular scripts in sequence to update the historical database and refresh static web outputs:
python3 python/fetch_air_quality.py
python3 python/transform_air_quality_data.py
python3 python/load_to_duckdb.py
python3 python/export_to_web.py

### Step 3: Launch the Local Dashboard
Start Python's built-in HTTP server from the root directory:
python3 -m http.server 8000

Open your browser and navigate to:
http://localhost:8000/app/index.html

---

## What I would do next

* **Workflow Automation:** Integrate GitHub Actions to execute the ingestion and transformation pipeline on a daily schedule, automatically building historical database increments and updating static web assets.
* **Automated Threshold Alerting:** Implement automated alerts (via Slack/Email webhooks) when key pollutants like NO2 or PM2.5 exceed UK national air quality threshold limits.
* **Expanded Telemetry Coverage:** Extend the data model to track multi-year historical trends across seasonal shifts to assist planners with long-term climate action targets.

---

## Where AI helped

* **Pipeline Architecture Review:** Assisted in evaluating lightweight database options, leading to the selection of DuckDB as a low-overhead, serverless storage engine.
* **Code Optimization:** Assisted in drafting efficient transformation logic for parsing nested JSON payloads into relational DuckDB schema.
* **Presentation & Documentation:** Helped organize technical workflows and presentation narrative points into clear, structured markdown documentation aligned with project requirements.
