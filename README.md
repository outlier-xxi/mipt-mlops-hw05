# README

ДЗ-5. Airflow

- Деплой Airflow
  - Репозиторий: https://github.com/outlier-xxi/mipt-mlops-airflow
  - GitHub Actions Deploy: https://github.com/outlier-xxi/mipt-mlops-airflow/actions


## Архитектура

Projects:

```mermaid
flowchart LR
    Airflow_Repo([mipt-mlops-airflow<br>repository]) --> |Deploy Airflow<br>Github Actions| Airflow[Airflow Server]
    DAG_Repo([mipt-mlops-hw05<br>repository]) --> |Deploy DAG<br>Github Actions| Airflow[Airflow Server]
```

DAG:

```mermaid
flowchart LR
    train_model --> evaluate --> deploy --> notify_success
```

## Структура проекта
