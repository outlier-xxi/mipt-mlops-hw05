# README

ДЗ-5. Airflow

- Деплой Airflow
  - Репозиторий: https://github.com/outlier-xxi/mipt-mlops-airflow
  - GitHub Actions Deploy: https://github.com/outlier-xxi/mipt-mlops-airflow/actions


## Архитектура

```mermaid
flowchart LR
    Client([Client]) --> ML[ML Service<br/>:8000]
    ML --> |metrics :8001| Prometheus[(Prometheus<br/>:9090)]
    Prometheus --> Grafana[Grafana<br/>:3000]
    Grafana --> |alerts| Telegram([Telegram])
```

## Структура проекта
