output "services" {
  description = "URL for running services"
  value = {
    pgadmin = "http://localhost:${var.pgadmin_port}"
  }
}

output "postgres_connection" {
  description = "PostgreSQL connection details (password omitted)"
  value = {
    name      = var.postgres_db
    host_name = "${var.project_name}-postgres"
    port      = 5432
    username  = var.postgres_user
  }
}
