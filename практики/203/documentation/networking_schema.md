# Схема сети контейнеров — TaskFlow

## Диаграмма

```mermaid
graph TD
    User["Пользователь (браузер)"]

    subgraph internal["Docker Network: internal"]
        App["app\npython:3.12-slim\n:8000"]
        DB["db\npostgres:16-alpine\n:5432"]
        Cache["cache\nredis:7-alpine\n:6379"]
    end

    User -->|"HTTP :8000"| App
    App -->|"SQL / psycopg2"| DB
    App -->|"Redis protocol"| Cache
```

## Описание сети

Все три сервиса находятся в изолированной bridge-сети `internal`. Наружу (на хост-машину) пробрасывается только порт `8000` сервиса `app` — БД и Redis недоступны извне.

| Сервис | Образ | Порт внутри сети | Порт на хосте |
| ------ | ----- | ---------------- | -------------- |
| `app` | `python:3.12-slim` | 8000 | 8000 |
| `db` | `postgres:16-alpine` | 5432 | — |
| `cache` | `redis:7-alpine` | 6379 | — |

## Volumes

| Volume | Смонтирован в | Назначение |
| ------ | ------------- | ---------- |
| `postgres_data` | `/var/lib/postgresql/data` | Персистентное хранение данных БД между перезапусками |

## Запуск

```bash
docker-compose up -d
```
