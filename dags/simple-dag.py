from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import GoogleCloudServiceAccountDictProfileMapping

import os
from datetime import datetime


airflow_home = os.environ["AIRFLOW_HOME"]

profile_config = ProfileConfig(
    profile_name="dbt-airflow-469721",  # substitua pelo nome do profile_config adequado *
    target_name="prod", # substitua pelo nome do target no seu profiles.yml
    profile_mapping=GoogleCloudServiceAccountDictProfileMapping(
        conn_id="project_01_gcloud_connection",  # substitua pelo nome da conexao criada no Airflow
        profile_args={
            "project": "dbt-airflow-469721",  # substitua pelo ID do seu projeto GCP
            "dataset": "prod" # substitua pelo prefixo (dev_, stg_, prod_) do seu dataset no BigQuery
        }
    )
)

my_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
        f"{airflow_home}/dags/dbt/project_01",  # substitua pelo caminho do seu projeto dbt (pasta do projeto dbt)
    ),
    profile_config=profile_config,  # substitua pelo nome do profile_config adequado *
    execution_config=ExecutionConfig(
        dbt_executable_path=f"{airflow_home}/dbt_venv/bin/dbt",
    ),
    # parametros normais da dag
    schedule="00 09 * * *", 
    start_date=datetime(2023, 1, 1),  
    catchup=False,  # nao ira processar execucoes antigas
    is_paused_upon_creation=True,  # Nasce pausada
    dag_id="simple-dag",  # substitua pelo nome do arquivo .py
    tags=["marketing"],  # tags para a dag (detalhes abaixo do nome da dag)
    default_args={"retries": 1},  # quantidade de tentativas em caso de falha
    max_active_tasks=2,
)
