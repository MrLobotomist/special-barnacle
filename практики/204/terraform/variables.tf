variable "image_tag" {
  description = "Docker image tag for the app"
  type        = string
  default     = "ghcr.io/mrlobotomist/special-barnacle:latest"
}

variable "postgres_password" {
  description = "PostgreSQL password"
  type        = string
  sensitive   = true
}

variable "postgres_db" {
  description = "PostgreSQL database name"
  type        = string
  default     = "taskflow"
}

variable "postgres_user" {
  description = "PostgreSQL user"
  type        = string
  default     = "postgres"
}

variable "app_port" {
  description = "Host port for the app"
  type        = number
  default     = 8000
}
