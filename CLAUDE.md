# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a dbt + Apache Airflow + BigQuery data pipeline orchestration project using Astronomer Cosmos for native integration. The project demonstrates modern data engineering practices with containerized development using Docker and Astro runtime.

## Core Commands

### Airflow Development
```bash
# Start Airflow development environment with Astronomer CLI
astro dev start

# Stop development environment  
astro dev stop

# Restart environment
astro dev restart

# View running containers
astro dev ps

# Access Airflow scheduler logs
astro dev logs scheduler

# Access Airflow webserver logs
astro dev logs webserver
```

### dbt Commands (within project_01 directory)
```bash
# Change to dbt project directory
cd dags/dbt/project_01

# Install dbt dependencies
dbt deps

# Debug dbt configuration
dbt debug

# Run all models
dbt run

# Run specific model
dbt run --models model_name

# Run tests
dbt test

# Full build (run + test)
dbt build

# Generate and serve documentation
dbt docs generate && dbt docs serve
```

### Testing
```bash
# Run Airflow DAG tests
pytest tests/dags/

# Validate DAG syntax
python dags/simple-dag.py

# Check for DAG import errors
astro dev bash
airflow dags list
```

## Project Architecture

### Technology Stack
- **Apache Airflow**: 3.0 runtime via Astronomer
- **dbt-bigquery**: 1.9.1 for data transformations
- **Astronomer Cosmos**: 1.10.2 for Airflow-dbt integration
- **Docker**: Containerized development environment
- **Google BigQuery**: Data warehouse
- **Python**: 3.9+ base runtime

### Directory Structure
```
├── dags/
│   ├── simple-dag.py              # Main Cosmos DAG configuration
│   └── dbt/
│       └── project_01/            # dbt project with models, tests, seeds
├── include/                       # Airflow include files
├── plugins/                       # Custom Airflow plugins
├── tests/
│   └── dags/                      # DAG validation tests
├── Dockerfile                     # Astro runtime with dbt installation
├── airflow_settings.yaml          # Local Airflow connections/variables
├── requirements.txt               # Python dependencies (Cosmos)
└── packages.txt                   # OS-level packages
```

### Key Components

**Cosmos Integration**: The `simple-dag.py` uses DbtDag to automatically convert dbt models into Airflow tasks, providing:
- Automatic task dependency resolution based on dbt model relationships
- Individual task monitoring and retry capabilities
- Integration with Airflow's scheduling and alerting

**dbt Project Structure**: Located in `dags/dbt/project_01/` following standard dbt conventions:
- `models/staging/`: Raw data transformations (materialized as tables)
- `models/intermediate/`: Business logic transformations (ephemeral)
- `models/marts/`: Final business models (materialized as tables)
- `seeds/`: Static reference data files
- `macros/`: Custom SQL macros

**BigQuery Integration**: Configured for Google BigQuery with service account authentication and schema-based organization (stg, int, marts, raw).

## Configuration Requirements

### Environment Variables
The BigQuery connection requires these environment variables (referenced in profiles.yml):
- Connection ID: `my_google_cloud_platform_connection` in Airflow
- Service account JSON file: `/usr/local/airflow/dags/dbt/project_01/dbt-airflow-469721-26c5256c1285.json`
- GCP Project ID: `dbt-airflow-469721`
- Target dataset: `prod`

### DAG Configuration
The main DAG (`simple-dag`) is configured with:
- Schedule: `0 21 * * *` (daily at 9 PM)
- Start date: January 1, 2023
- Retries: 1 attempt on failure
- Tags: `["marketing"]`
- No catchup for historical runs

### Development Setup
1. Ensure Docker is running
2. Use `astro dev start` to launch local Airflow
3. Access Airflow UI at http://localhost:8080 (admin/admin)
4. Configure Google Cloud connection in Airflow UI
5. Place service account JSON in the specified path
6. Test DAG by triggering manually

## Important Notes

- The dbt virtual environment is pre-installed in Docker at `/usr/local/airflow/dbt_venv/`
- DAG tests expect retries >= 2, but current configuration has retries: 1
- Service account credentials should be properly secured and not committed to repository
- The project uses fixed versions (Cosmos 1.10.2, dbt-bigquery 1.9.1) for stability