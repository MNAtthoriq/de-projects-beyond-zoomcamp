output "postgres_network_name" {
  description = "Name of the Docker network shared across all services"
  value       = docker_network.postgres_network.name
}