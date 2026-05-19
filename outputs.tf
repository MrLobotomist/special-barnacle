output "app_url" {
  description = "Application URL"
  value       = "http://localhost:${var.app_port}"
}

output "app_container_name" {
  description = "App container name"
  value       = docker_container.app.name
}

output "app_container_id" {
  description = "App container ID"
  value       = docker_container.app.id
}

output "db_container_name" {
  description = "PostgreSQL container name"
  value       = docker_container.db.name
}

output "db_container_id" {
  description = "PostgreSQL container ID"
  value       = docker_container.db.id
}

output "network_id" {
  description = "Internal network ID"
  value       = docker_network.internal.id
}
