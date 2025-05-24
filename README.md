# Airflow 3.0.1 Docker Compose Setup

This repository provides a battle-tested Docker Compose setup for Apache Airflow 3.0.1, backed by PostgreSQL, with optional pgAdmin for database management. It automates environment configuration, volume mounting, and user-permission handling to give you a zero-hassle local Airflow development environment.

### features

* run airflow in docker
* manage all service in docker-compose 
* call docker images inside airflow DAG 

## 🚀 Quick Start

### 1. Clone the repo
```shell

git clone git@github.com:Jiansiyu/airflow_docker_compose.git
cd airflow_docker_compose

```

### 2. Generate your `.env` file

```shell


bash start_docker.sh

```

### 3.Launch services

````shell

docker compose up -d

````


### 4. Access the UIs

* Airflow (API server & web UI): http://localhost:8080
  * Username: `airflow`
  * Password: `airflow`

* pgAdmin (if enabled): http://localhost:5050
  * Email: `admin@admin.com` 
  * Password: `admin`


## 📦 Project Structure

```shell
.
├── docker-compose.yaml     # Main Compose configuration
├── .env.template           # Template for environment variables
├── start_docker.sh         # Generates .env and (optional) spins up Compose
├── dags/                   # Your Airflow DAG definitions
├── logs/                   # Airflow scheduler & task logs
├── config/                 # airflow.cfg and custom configs
└── plugins/                # Custom Airflow plugins

```

## ⚙️ Configuration
### 1. Environment Variables

Edit `.env.template` to suit your environment, then run `start_docker.sh`:

* **AIRFLOW_UID**, **AIRFLOW_GID** — Host user/group IDs for proper file ownership

* **DOCKER_GID** — Host Docker group ID for DockerOperator permissions

* **AIRFLOW_WWW_USER_USERNAME** / **PASSWORD** — Web UI credentials

* **POSTGRES_USER** / **PASSWORD** / **DB** — Metadata database credentials

* **PGADMIN_DEFAULT_EMAIL** / **PASSWORD** — pgAdmin credentials

* **ENABLE_PGADMIN** — Set to true to expose pgAdmin under profile pgadmin

### 2. Compose Profiles

* default: Airflow + PostgreSQL

* pgadmin: Add --profile pgadmin to enable pgAdmin service


## 📂 Example DAGs

### 1. Basic ETL Pipeline
A template demonstrating:

* Python operators 
* Connection management 
* Data extraction, transformation, and loading

> Location: dags/example_etl_dag.py

### 2. Docker-based Task
Runs a containerized task via DockerOperator.
Ensure:

* Docker socket is mounted

* apache-airflow-providers-docker is installed

* Appropriate group permissions (see Troubleshooting)

> Location: dags/hello_docker.py

## 🛠️ Services
| Service                   | Description                                               |
| ------------------------- | --------------------------------------------------------- |
| **postgres**              | PostgreSQL metadata database                              |
| **pgadmin**               | Web UI for PostgreSQL (enabled via `pgadmin` profile)     |
| **airflow-init**          | Initializes directories, permissions, and default configs |
| **airflow-scheduler**     | Schedules and triggers task execution                     |
| **airflow-apiserver**     | Exposes Airflow’s REST API and web UI                     |
| **airflow-dag-processor** | Parses and validates your DAG files                       |
| **airflow-triggerer**     | Handles deferrable and trigger-based operators            |
| **airflow-cli**           | CLI container for debugging (use `--profile debug`)       |

## 🔧 Customization
* Custom airflow.cfg — Drop overrides into config/ (mapped to /opt/airflow/config).

* Additional Python packages — Add them to _PIP_ADDITIONAL_REQUIREMENTS in your .env.

* New DAGs — Simply place your .py files inside the dags/ folder; they’ll be auto-detected.