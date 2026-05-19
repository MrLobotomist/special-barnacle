# Схема инфраструктуры — Terraform

## Граф ресурсов

```mermaid
graph TD
    subgraph Terraform State
        NET[docker_network.internal<br/>bridge: taskflow_internal]
        VOL[docker_volume.postgres_data]

        IMG_PG[docker_image.postgres<br/>postgres:16-alpine]
        IMG_RD[docker_image.redis<br/>redis:7-alpine]
        IMG_APP[docker_image.app<br/>ghcr.io/mrlobotomist/special-barnacle:latest]

        DB[docker_container.db<br/>taskflow_db]
        CACHE[docker_container.cache<br/>taskflow_cache]
        APP[docker_container.app<br/>taskflow_app]
    end

    HOST[Хост :8000] -->|ports 8000:8000| APP

    IMG_PG --> DB
    IMG_RD --> CACHE
    IMG_APP --> APP

    VOL --> DB
    NET --> DB
    NET --> CACHE
    NET --> APP

    DB --> APP
    CACHE --> APP
```

## Порядок создания ресурсов

1. `docker_network.internal` — сеть создаётся первой
2. `docker_volume.postgres_data` — том независим от контейнеров
3. `docker_container.db` — зависит от сети и тома
4. `docker_container.cache` — зависит от сети
5. `docker_container.app` — зависит от db и cache (`depends_on`)

Terraform автоматически определяет порядок по графу зависимостей и создаёт независимые ресурсы параллельно.

## Сеть

Все три контейнера подключены к сети `taskflow_internal` (bridge). Снаружи доступен только порт `8000` приложения. PostgreSQL и Redis не публикуют порты на хост.
