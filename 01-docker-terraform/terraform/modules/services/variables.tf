variable "project_name" {
  description = "Prefix used for all resource name"
  type        = string
}

variable "postgres_network_name" {
  description = "Name of the Docker network shared across all services"
  type        = string
}

variable "postgres_data_name" {
  description = "Database for PostgreSQL"
  type        = string
}

variable "pgadmin_data_name" {
  description = "Database for pgAdmin"
  type        = string
}

variable "postgres_user" {
  description = "PostgreSQL username"
  type        = string
}

variable "postgres_password" {
  description = "PostgreSQL password"
  type        = string
  sensitive   = true
}

variable "postgres_db" {
  description = "PostgreSQL database"
  type        = string
}

variable "pgadmin_user" {
  description = "pgAdmin username"
  type        = string
}

variable "pgadmin_password" {
  description = "pgAdmin password"
  type        = string
  sensitive   = true
}

variable "pgadmin_port" {
  description = "pgAdmin external port"
  type        = number
}