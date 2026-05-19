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

## State Management

Terraform хранит текущее состояние инфраструктуры в файле `terraform.tfstate`. При каждом `plan` и `apply` Terraform сравнивает три источника:

1. **Конфигурация** (`.tf` файлы) — желаемое состояние
2. **State-файл** (`terraform.tfstate`) — последнее известное состояние
3. **Реальная инфраструктура** — опрашивается через провайдер

На основе этого сравнения Terraform вычисляет дельту и применяет только необходимые изменения.

**Почему `terraform.tfstate` нельзя хранить в публичном репозитории:**

State-файл содержит в открытом виде все значения ресурсов, включая те, что помечены `sensitive = true` в конфигурации (пароли, токены, строки подключения). Terraform записывает их в state без маскировки — это сделано намеренно, чтобы корректно вычислять дельту при следующем apply. Публикация state в открытом репо означает утечку всех секретов инфраструктуры.

## Drift Detection

Drift — это расхождение между реальным состоянием инфраструктуры и тем, что зафиксировано в `terraform.tfstate`.

**Демонстрация:** в ходе работы контейнеры `taskflow_db` и `taskflow_cache` были пересозданы вручную через `docker compose down`. При следующем `terraform plan` Terraform обнаружил drift:

```
Note: Objects have changed outside of Terraform

# docker_container.app has been deleted
- resource "docker_container" "app" {
    - id = "de0c29eb..." -> null
  }
```

Terraform автоматически предложил план восстановления (`3 to add`) и привёл инфраструктуру к декларативному состоянию через `terraform apply`. docker-compose не имеет аналогичного механизма — он не знает, что изменилось за пределами его собственного `up/down`.
