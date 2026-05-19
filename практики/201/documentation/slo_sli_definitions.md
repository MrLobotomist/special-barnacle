# Определение метрик успеха проекта (SLI / SLO)

## SLI — Service Level Indicators

Что именно измеряем:

| # | SLI | Описание | Инструмент |
| - | --- | -------- | ---------- |
| 1 | **API Availability** | Доля успешных HTTP-ответов (2xx/3xx) от общего числа запросов | Uptime Robot |
| 2 | **API Response Time (p95)** | 95-й перцентиль времени ответа на GET /tasks | FastAPI middleware |
| 3 | **Deployment Success Rate** | Доля успешных деплоев (pipeline завершился без ошибок) | GitHub Actions |
| 4 | **Error Rate** | Доля ответов 5xx от общего числа запросов | Логи приложения |

## SLO — Service Level Objectives

Целевые значения:

| SLI | SLO | Окно измерения |
| --- | --- | -------------- |
| API Availability | ≥ 99.5% | 30 дней |
| API Response Time (p95) | ≤ 300 мс | 24 часа |
| Deployment Success Rate | ≥ 95% | 30 дней |
| Error Rate | ≤ 0.5% | 24 часа |

## Error Budget

При SLO Availability = 99.5% за 30 дней:

- Допустимое время простоя: **30 × 24 × 0.005 = 3.6 часа/месяц**

## Как будем измерять

- Логи FastAPI → stdout → файл `app.log`
- GitHub Actions предоставляет метрики деплоев из коробки
- Uptime Robot для внешнего мониторинга доступности
