# TaskFlow — Практика 203

## Образ

Публичный образ: `ghcr.io/mrlobotomist/special-barnacle:latest`

```bash
docker pull ghcr.io/mrlobotomist/special-barnacle:latest
```

## Запуск всего проекта

```bash
docker-compose up -d
```

Приложение будет доступно на `http://localhost:8000`.

## Сервисы

| Сервис | Образ | Назначение |
| ------ | ----- | ---------- |
| `app` | `ghcr.io/mrlobotomist/special-barnacle:latest` | FastAPI REST API |
| `db` | `postgres:16-alpine` | База данных |
| `cache` | `redis:7-alpine` | Кэш |

## CI: автоматическая сборка и публикация

После успешного прохождения тестов пайплайн автоматически собирает и публикует образ в GHCR. Конфигурация: [`.github/workflows/ci.yml`](https://github.com/MrLobotomist/special-barnacle/blob/main/.github/workflows/ci.yml)
