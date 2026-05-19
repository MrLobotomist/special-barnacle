# Стратегия IaC — TaskFlow

## Зачем IaC вместо docker-compose

| Критерий | docker-compose | Terraform |
| -------- | -------------- | --------- |
| Декларативность | Частичная | Полная (plan/apply) |
| State-файл | Отсутствует | `terraform.tfstate` — знает текущее состояние |
| Идемпотентность | Нет (`up` всегда пересоздаёт) | Да (apply применяет только дельту) |
| Drift detection | Нет | Да (`terraform plan` показывает расхождение) |
| Переменные и типизация | Env-файлы | `variables.tf` с типами и валидацией |
| Масштабируемость | Только Docker | AWS, GCP, K8s, любые провайдеры |

## Провайдер

`kreuzwerker/docker ~> 3.0` — единственный поддерживаемый провайдер Docker для Terraform 1.x. Управляет ресурсами: `docker_container`, `docker_image`, `docker_network`, `docker_volume`.

## Ресурсы

| Ресурс Terraform | Соответствие docker-compose |
| ---------------- | --------------------------- |
| `docker_network.internal` | `networks.internal` (bridge) |
| `docker_volume.postgres_data` | `volumes.postgres_data` |
| `docker_container.db` | `services.db` (postgres:16-alpine) |
| `docker_container.cache` | `services.cache` (redis:7-alpine) |
| `docker_container.app` | `services.app` (ghcr.io/mrlobotomist/special-barnacle) |

## Переменные

Чувствительные данные (`postgres_password`) помечены `sensitive = true` — Terraform скрывает их из вывода plan/apply. В продакшене передаются через переменные окружения (`TF_VAR_postgres_password`) или секреты CI, не через `terraform.tfvars`.

## Жизненный цикл

```
terraform init    # скачать провайдер kreuzwerker/docker
terraform plan    # показать что будет создано (dry-run)
terraform apply   # создать/обновить ресурсы
terraform destroy # удалить все ресурсы
```

`terraform plan` перед каждым `apply` — ключевое преимущество перед docker-compose: видно заранее, что изменится, без риска случайного downtime.
