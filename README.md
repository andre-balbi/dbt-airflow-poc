# dbt + Airflow + BigQuery | Data Pipeline Orchestration

[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)](https://airflow.apache.org/)
[![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![Google BigQuery](https://img.shields.io/badge/Google%20BigQuery-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/bigquery)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## 📋 Descrição do Projeto

Pipeline de dados moderno que combina **Apache Airflow** para orquestração de workflows com **dbt** (data build tool) para transformações de dados no **Google BigQuery**. O projeto utiliza a biblioteca **Cosmos** para integração nativa entre Airflow e dbt, proporcionando observabilidade completa e controle granular sobre as transformações de dados.

**Caso de uso:** Automação de pipelines de dados em ambiente de produção com capacidade de processamento escalável, monitoramento de qualidade e versionamento de transformações.

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Função |
|------------|--------|---------|
| **Apache Airflow** | 12.7.1 | Orquestração de workflows |
| **dbt Core** | 1.9.1 | Transformações SQL e modelagem |
| **Astronomer Cosmos** | 1.10.2 | Integração Airflow + dbt |
| **Google BigQuery** | - | Data Warehouse |
| **Docker** | Latest | Containerização |
| **Python** | 3.9+ | Linguagem principal |

## 📁 Arquitetura do Projeto

```
dbt-airflow-02/
├── dags/
│   └── simple-dag.py          # DAG principal com configuração Cosmos
├── dbt/
│   └── nome-do-seu-projeto/            # Projeto dbt com models e testes
├── include/                   # Arquivos auxiliares
├── plugins/                   # Plugins customizados Airflow
├── tests/
│   └── dags/                  # Testes das DAGs
├── airflow_settings.yaml      # Configurações locais
├── CLAUDE.md                  # Documentação técnica
└── requirements.txt           # Dependências Python
```

## ⚡ Funcionalidades Principais

- **Orquestração Automatizada**: DAGs Airflow com scheduling configurável
- **Transformações dbt**: Models SQL organizados em camadas (staging, intermediate, marts)
- **Integração Cosmos**: Conversão automática de models dbt em tasks Airflow
- **Observabilidade**: Monitoramento completo via interface Airflow
- **Ambiente Isolado**: Containerização Docker para consistência

## 🔧 Pré-requisitos

- **Docker** e **Docker Compose**
- **Conta Google Cloud** com BigQuery habilitado
- **Service Account** GCP com permissões BigQuery

## 🚀 Instalação e Configuração

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/dbt-airflow.git
cd dbt-airflow
```

### 2. Configurar seu Projeto

#### 📂 Estrutura de Projetos dbt
Os projetos dbt devem ser organizados em `dbt/nome-do-seu-projeto/`:
```
dbt/
├── nome-do-seu-projeto/          # Seu projeto dbt principal
│   ├── dbt_project.yml
│   ├── models/
│   ├── tests/
│   └── ...
├── outro_projeto/       # Projetos adicionais (opcional)
└── ...
```

#### ⚙️ Configurações Obrigatórias no DAG
Edite `dags/simple-dag.py` com suas configurações específicas:

```python
profile_config_01 = ProfileConfig(
    profile_name="nome-do-seu-projeto",           # ✏️ Nome do seu projeto dbt
    target_name="prod",                   # ✏️ Ambiente (dev/prod)
    profile_mapping=GoogleCloudServiceAccountFileProfileMapping(
        conn_id="my_google_cloud_platform_connection",  # ✏️ ID da conexão Airflow
        profile_args={
            "project": "seu-projeto-gcp-123",       # ✏️ ID do projeto GCP
            "dataset": "prod",                      # ✏️ Dataset BigQuery
            "keyfile": "/usr/local/airflow/dbt/nome-do-seu-projeto/service-account.json"  # ✏️ Chave de serviço (preferencialmente na raiz do projeto dbt)
        }
    )
)

my_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
        f"{airflow_home}/dbt/nome-do-seu-projeto",  # ✏️ Caminho do projeto dbt
    ),
    dag_id="seu-dag-id",                    # ✏️ ID único da DAG
    schedule_interval="@daily",             # ✏️ Frequência de execução
    start_date=datetime(2023, 1, 1),        # ✏️ Data de início
    tags=["seu_time", "etl"],              # ✏️ Tags para organização
)
```

#### 🔑 Configurar Credenciais BigQuery
```bash
# Definir variáveis de ambiente para autenticação
export DBT_ENV_SECRET_PROJECT_ID="seu-projeto-gcp"
export DBT_ENV_SECRET_CLIENT_EMAIL="sua-service-account@projeto.iam.gserviceaccount.com"
export DBT_ENV_SECRET_PRIVATE_KEY="sua-chave-privada"
# ... outras variáveis conforme CLAUDE.md
```

### 3. Iniciar Ambiente de Desenvolvimento
```bash
# Com Astronomer CLI (recomendado)
astro dev start
```

### 4. Acessar Interfaces
- **Airflow UI**: http://localhost:8080
  - Usuário: `admin` | Senha: `admin`
- **Postgres DB**: localhost:5432
  - Database: `postgres` | Usuário: `postgres` | Senha: `postgres`

## 💡 Como Usar

### Executar Pipeline Completo
```bash
# Via Airflow UI
1. Acesse http://localhost:8080
2. Localize a DAG "simple-dag"
3. Ative o toggle da DAG
4. Clique em "Trigger DAG"
```

### Comandos dbt Locais
```bash
# Navegar para o seu projeto dbt
cd dbt/nome-do-seu-projeto

# Instalar dependências
dbt deps

# Executar todos os models
dbt run

# Executar testes
dbt test

# Gerar documentação
dbt docs generate && dbt docs serve
```

### Monitoramento
```python
# Configuração da DAG (dags/simple-dag.py)
schedule_interval="@daily"    # Execução diária
start_date=datetime(2023, 1, 1)
catchup=False                 # Não processar execuções antigas
default_args={"retries": 1}   # 1 tentativa em caso de falha
```

## 📊 Exemplo de Implementação

### Estrutura de um Model dbt
```sql
-- models/staging/stg_orders.sql
{{ config(materialized='table') }}

SELECT 
    order_id,
    customer_id,
    order_date,
    total_amount,
    {{ dbt_utils.generate_surrogate_key(['order_id', 'customer_id']) }} as order_key
FROM {{ ref('raw_orders') }}
WHERE order_date >= '2023-01-01'
```

### Configuração Cosmos
```python
# Integração automática dbt → Airflow
my_cosmos_dag = DbtDag(
    project_config=ProjectConfig(f"{airflow_home}/dbt/nome-do-seu-projeto"),
    profile_config=profile_config_01,
    execution_config=ExecutionConfig(
        dbt_executable_path=f"{airflow_home}/dbt_venv/bin/dbt"
    ),
    schedule_interval="@daily",
    dag_id="simple-dag",
    tags=["marketing", "etl"]
)
```

## 🎯 Destaques Técnicos

- **Arquitetura de Dados Moderna**: Implementação ELT com dbt
- **DevOps para Dados**: Versionamento, testes e CI/CD
- **Escalabilidade**: Processamento distribuído BigQuery
- **Observabilidade**: Logging e monitoramento integrados
- **Qualidade de Dados**: Testes automatizados dbt
- **Versionamento Fixo**: Cosmos 1.10.2 e dbt-bigquery 1.9.1 para estabilidade

## 📝 Checklist de Configuração

Antes de executar o projeto, verifique:

- [ ] Projeto dbt criado em `dbt/nome-do-seu-projeto/`
- [ ] Arquivo `dags/simple-dag.py` configurado com seus dados
- [ ] Credenciais GCP definidas nas variáveis de ambiente
- [ ] Service Account com permissões BigQuery
- [ ] Conexão Airflow configurada (`my_google_cloud_platform_connection`)

## 📈 Próximos Passos

- [ ] Implementar testes de qualidade de dados
- [ ] Configurar alertas via Slack/Email
- [ ] Deploy em ambiente Cloud (Astronomer/Cloud Composer)
- [ ] Adicionar models de machine learning

## 📧 Contato

**Diego Rebalbi**
- 📧 Email: [seu-email@exemplo.com]
- 💼 LinkedIn: [linkedin.com/in/seu-perfil]
- 🐙 GitHub: [github.com/seu-usuario]

---

⭐ **Se este projeto foi útil, deixe uma estrela!**