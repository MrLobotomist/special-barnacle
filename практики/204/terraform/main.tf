resource "docker_network" "internal" {
  name   = "taskflow_internal"
  driver = "bridge"
}

resource "docker_volume" "postgres_data" {
  name = "taskflow_postgres_data"
}

resource "docker_image" "postgres" {
  name         = "postgres:16-alpine"
  keep_locally = true
}

resource "docker_image" "redis" {
  name         = "redis:7-alpine"
  keep_locally = true
}

resource "docker_image" "app" {
  name         = var.image_tag
  keep_locally = true
}

resource "docker_container" "db" {
  name  = "taskflow_db"
  image = docker_image.postgres.image_id

  env = [
    "POSTGRES_DB=${var.postgres_db}",
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
  ]

  volumes {
    volume_name    = docker_volume.postgres_data.name
    container_path = "/var/lib/postgresql/data"
  }

  networks_advanced {
    name = docker_network.internal.name
  }

  healthcheck {
    test         = ["CMD-SHELL", "pg_isready -U ${var.postgres_user}"]
    interval     = "5s"
    timeout      = "5s"
    retries      = 5
    start_period = "10s"
  }

  restart = "unless-stopped"
}

resource "docker_container" "cache" {
  name  = "taskflow_cache"
  image = docker_image.redis.image_id

  networks_advanced {
    name = docker_network.internal.name
  }

  restart = "unless-stopped"
}

resource "docker_container" "app" {
  name  = "taskflow_app"
  image = docker_image.app.image_id

  env = [
    "DATABASE_URL=postgresql://${var.postgres_user}:${var.postgres_password}@${docker_container.db.name}:5432/${var.postgres_db}",
    "REDIS_URL=redis://${docker_container.cache.name}:6379",
  ]

  ports {
    internal = 8000
    external = var.app_port
  }

  networks_advanced {
    name = docker_network.internal.name
  }

  restart = "unless-stopped"

  depends_on = [docker_container.db, docker_container.cache]
}
