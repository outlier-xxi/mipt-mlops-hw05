from datetime import datetime

import requests
from airflow import DAG
from airflow.models import Variables
from airflow.operators.python import PythonOperator


def train_model():
    config = Variables.get("ml_retrain_pipeline_config", deserialize_json=True)
    model_version = config.get('MODEL_VERSION')
    print(f"Модель обучена: {model_version}")

def evaluate_model():
    config = Variables.get("ml_retrain_pipeline_config", deserialize_json=True)
    model_version = config.get('MODEL_VERSION')
    print(f"Модель оценена, метрики в норме: {model_version}")

def deploy_model():
    config = Variables.get("ml_retrain_pipeline_config", deserialize_json=True)
    model_version = config.get('MODEL_VERSION')
    print(f"Модель выведена в продакшен: {model_version}")  

def send_telegram_message():
    config = Variables.get("ml_retrain_pipeline_config", deserialize_json=True)
    token = config.get("TELEGRAM_TOKEN")
    chat_id = config.get("TELEGRAM_CHAT_ID")
    model_version = config.get('MODEL_VERSION')

    message = f"Новая модель в продакшене! Версия {model_version}"
    requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}")


with DAG(
    dag_id="ml_retrain_pipeline",
    start_date=datetime(2025, 12, 20),
    schedule_interval="@daily",
    catchup=False,
    
) as dag:

    train = PythonOperator(task_id="train_model", python_callable=train_model)
    evaluate = PythonOperator(task_id="evaluate_model", python_callable=evaluate_model)
    deploy = PythonOperator(task_id="deploy_model", python_callable=deploy_model)
    notify_success = PythonOperator(
        task_id="notify_success",
        python_callable=send_telegram_message
    )

    train >> evaluate >> deploy >> notify_success
