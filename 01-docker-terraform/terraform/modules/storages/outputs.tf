output "postgres_data_name" {
  description = "Database for PostgreSQL"
  value       = docker_volume.postgres_data.name
}

output "pgadmin_data_name" {
  description = "Database for pgAdmin"
  value       = docker_volume.pgadmin_data.name
}