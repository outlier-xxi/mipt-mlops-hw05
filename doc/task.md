Домашнее задание 5. Модификация DAG в Airflow для уведомлений о выводе новой модели в продакшен


- настроит DAG, который собирает данные, обучает модель и регистрирует артефакты;
- реализует проверки качества и условную логику обновления модели;
- создаст минимальную IaC-конфигурацию для развертывания необходимых ресурсов;
- подключит CI/CD для автоматической проверки и применения изменений в конвейере.

# Как выполнять задание

## Шаг 1. Подготовить базовый DAG. 

Используйте готовый пайплайн из семинара Airflow retraining. Файл: dags/ml_retrain_pipeline.py.

Пример структуры DAG:

```python
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
```

## Шаг 2. Добавить уведомление о деплое. 

Создайте задачу notify_success, которая сработает после успешного выполнения deploy_model.

Вариант A — email:

```python
from airflow.operators.email import EmailOperator

notify = EmailOperator(
    task_id="notify_success",
    to="mlops-team@example.com",
    subject="Новая модель в продакшене",
    html_content="Версия модели <b>v2.3.1</b> успешно задеплоена и доступна через API."
)
```

Вариант B — Telegram (через HTTP-запрос):

```python
import requests
from airflow.operators.python import PythonOperator

def send_telegram_message():
    token = "YOUR_TELEGRAM_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    message = "Новая модель в продакшене! Версия v2.3.1"
    requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}")

notify = PythonOperator(
    task_id="notify_success",
    python_callable=send_telegram_message
)
```

Добавьте зависимость:

deploy >> notify

## Шаг 4. Использовать переменную окружения для версии модели. 

Добавьте в DAG:

```python
import os

MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")
```

И модифицируйте текст уведомления:

html_content=f"Новая модель <b>{MODEL_VERSION}</b> успешно развернута"

## Рекомендации

- Тестируйте DAG локально с помощью airflow tasks test ml_retrain_pipeline deploy_model.
- В настройках Airflow можно указать SMTP-сервер для EmailOperator.
- Для Telegram рекомендуется создать бота через @BotFather.
- Можно комбинировать несколько уведомлений.
- Не забудьте проверить логи в Airflow UI при тестировании уведомлений.

## Формат сдачи

- Файл ml_retrain_pipeline.py с обновленным DAG.
- Скриншот успешного запуска DAG с задачей notify_success в Airflow UI.
- Краткое описание способа уведомления (email, Telegram) в отчете или README.

