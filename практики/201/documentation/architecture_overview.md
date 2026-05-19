# Архитектурный обзор — TaskFlow

## Компоненты системы

```mermaid
graph LR
    User["Пользователь\n(браузер)"]
    API["FastAPI\n(Python 3.12)"]
    DB["SQLite\n(файл tasks.db)"]
    GHA["GitHub Actions\n(CI)"]

    User -->|HTTP| API
    API -->|SQL| DB
    GHA -->|pytest| API
```

## Описание компонентов

### FastAPI (Backend)

- REST API: CRUD для задач (`/tasks`)
- Хранение через встроенный `sqlite3`

### SQLite

- Один файл `tasks.db` рядом с приложением
- Не требует отдельного сервера
