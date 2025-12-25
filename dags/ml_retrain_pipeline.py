from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def train_model():
    print("Модель обучена")

def evaluate_model():
    print("Модель оценена, метрики в норме")

def deploy_model():
    print("Модель выведена в продакшен")

with DAG(
    dag_id="ml_retrain_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    train = PythonOperator(task_id="train_model", python_callable=train_model)
    evaluate = PythonOperator(task_id="evaluate_model", python_callable=evaluate_model)
    deploy = PythonOperator(task_id="deploy_model", python_callable=deploy_model)

    train >> evaluate >> deploy
    