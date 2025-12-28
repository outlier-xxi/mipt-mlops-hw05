from datetime import datetime

import requests
from airflow import DAG
from airflow.sdk import Variable
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator


def deploy():
    config = Variable.get("ml_retrain_pipeline_config", deserialize_json=True)
    model_version = config.get('MODEL_VERSION')
    print(f"Модель выведена в продакшен: {model_version}")  

def send_telegram_message():
    config = Variable.get("ml_retrain_pipeline_config", deserialize_json=True)
    token = config.get("TELEGRAM_TOKEN")
    chat_id = config.get("TELEGRAM_CHAT_ID")
    model_version = config.get('MODEL_VERSION')

    message = f"Новая модель в продакшене! Версия {model_version}"
    print(f"Отправка сообщения в Telegram: {message}")
    response = requests.get(
        f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    )
    print(f"Результат отправки: {response.json()}")

with DAG(
    dag_id="ml_retrain_pipeline",
    start_date=datetime(2025, 12, 20),
    schedule="@daily",
    catchup=False,
    
) as dag:
    config = Variable.get("ml_retrain_pipeline_config", deserialize_json=True)
    model_version = config.get('MODEL_VERSION')
    image_name = config.get('IMAGE_NAME', "ghcr.io/outlier-xxi/ml-retrain:latest")

    train = DockerOperator(
        task_id="train", 
        image=image_name, 
        command="python src/tasks/train.py",
        docker_conn_id="ghcr.io",    # Airflow connection to GHCR
        force_pull=True,
        environment=config,
    )

    evaluate = DockerOperator(
        task_id="evaluate", 
        image=image_name, 
        command="python src/tasks/evaluate.py",
        docker_conn_id="ghcr.io",    # Airflow connection to GHCR
        force_pull=True,
        environment=config,
    )

    deploy = PythonOperator(
        task_id="deploy", python_callable=deploy
    )

    notify_success = PythonOperator(
        task_id="notify_success",
        python_callable=send_telegram_message
    )

    train >> evaluate >> deploy >> notify_success
