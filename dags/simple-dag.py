from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import GoogleCloudServiceAccountFileProfileMapping

import os
from datetime import datetime

airflow_home = os.environ["AIRFLOW_HOME"]

profile_config_01 = ProfileConfig(  # substitua pelo nome do profile_config adequado *
    profile_name="project_01",  # substitua pelo nome do projeto (pasta do dbt)
    target_name="prod", # substitua pelo nome do target no seu profiles.yml
    profile_mapping=GoogleCloudServiceAccountFileProfileMapping(
        conn_id="my_google_cloud_platform_connection",
        profile_args={
            "project": "dbt-airflow-469721",  # substitua pelo ID do seu projeto GCP
            "dataset": "prod",  # substitua pelo prefixo (dev_, stg_, prod_) do seu dataset no BigQuery
            "keyfile": "/usr/local/airflow/dbt/project_01/dbt-airflow-469721-26c5256c1285.json"  # substitua pelo caminho (docker) do seu arquivo de chave de conta de serviço
        }
    )
)

my_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
        f"{airflow_home}/dbt/project_01",  # substitua pelo caminho do seu projeto dbt (pasta do projeto dbt)
    ),
    profile_config=profile_config_01,  # substitua pelo nome do profile_config adequado *
    execution_config=ExecutionConfig(
        dbt_executable_path=f"{airflow_home}/dbt_venv/bin/dbt",
    ),
    # normal dag parameters
    schedule="@daily",  # substitua pelo schedule_interval desejado para a DAG
    start_date=datetime(2023, 1, 1),  # substitua pela data de inicio
    catchup=False,  # nao ira processar execucoes antigas
    dag_id="simple-dag",  # substitua pelo nome do arquivo .py
    tags=["marketing"],  # tags para a dag (detalhes abaixo do nome da dag)
    default_args={"retries": 1},  # quantidade de tentativas em caso de falha
)