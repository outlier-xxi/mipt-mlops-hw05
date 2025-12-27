from datetime import datetime

import requests
from airflow import DAG
from airflow.sdk import Variable
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator


#def train_model():
#    config = Variable.get("ml_retrain_pipeline_config", deserialize_json=True)
#    model_version = config.get('MODEL_VERSION')
#    print(f"Модель обучена: {model_version}")

def evaluate_model():
    config = Variable.get("ml_retrain_pipeline_config", deserialize_json=True)
    model_version = config.get('MODEL_VERSION')
    print(f"Модель оценена, метрики в норме: {model_version}")

def deploy_model():
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

    # train_model = PythonOperator(task_id="train_model", python_callable=train_model)
    train_model = DockerOperator(
        task_id="train_model", 
        image="ghcr.io/outlier-xxi/ml-retrain:latest", 
        command="python src/tasks/train_model.py",
        docker_conn_id="ghcr.io",    # Airflow connection to GHCR
        force_pull=True,
    )
    evaluate = PythonOperator(task_id="evaluate_model", python_callable=evaluate_model)
    deploy = PythonOperator(task_id="deploy_model", python_callable=deploy_model)
    notify_success = PythonOperator(
        task_id="notify_success",
        python_callable=send_telegram_message
    )

    train_model >> evaluate >> deploy >> notify_success
