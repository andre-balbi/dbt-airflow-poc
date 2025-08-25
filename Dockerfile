FROM astrocrpublic.azurecr.io/runtime:3.0-9

# install dbt into a virtual environment
RUN python -m venv dbt_venv && source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-bigquery==1.9.1 && deactivate