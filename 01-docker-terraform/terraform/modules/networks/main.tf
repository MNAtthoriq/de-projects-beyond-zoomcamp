terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.2.0"
    }
  }
}

resource "docker_network" "postgres_network" {
  name = "${var.project_name}-postgres-network"
}