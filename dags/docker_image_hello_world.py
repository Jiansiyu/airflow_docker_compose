# dags/hello_docker.py

from datetime import datetime
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'owner': 'you',
    'start_date': datetime(2025, 5, 24),
}

with DAG(
    'hello_docker',
    default_args=default_args,
    catchup=False,
) as dag:

    t1 = DockerOperator(
        task_id='run_hello',
        image='hello-world:latest',      # your locally-built image
        api_version='auto',
        auto_remove='force',                   # clean up container when done
        # command='echo "Hello from inside Docker!"',
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
    )
