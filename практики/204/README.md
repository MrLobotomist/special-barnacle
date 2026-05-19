# Practice 204 — Terraform IaC

Инфраструктура TaskFlow описана через Terraform с провайдером `kreuzwerker/docker`.

## Быстрый старт

```bash
cd практики/204/terraform

terraform init
terraform plan
terraform apply
```

Приложение доступно на http://localhost:8000

## Остановка

```bash
terraform destroy
```

## Переменные

| Переменная | По умолчанию | Описание |
| ---------- | ------------ | -------- |
| `image_tag` | `ghcr.io/mrlobotomist/special-barnacle:latest` | Образ приложения |
| `postgres_password` | `postgres` | Пароль PostgreSQL |
| `postgres_db` | `taskflow` | Имя БД |
| `postgres_user` | `postgres` | Пользователь БД |
| `app_port` | `8000` | Порт приложения на хосте |

## Структура

```
terraform/
  providers.tf   — провайдер kreuzwerker/docker
  variables.tf   — входные переменные
  main.tf        — ресурсы: сеть, тома, контейнеры
  outputs.tf     — URL приложения и ID контейнеров
  terraform.tfvars — значения по умолчанию
documentation/
  iac_strategy.md          — сравнение Terraform vs docker-compose
  infrastructure_schema.md — граф ресурсов (Mermaid)
```
