terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.2.0"
    }
  }
}

resource "docker_image" "postgres" {
  name         = "postgres:18"
  keep_locally = true
}

resource "docker_container" "postgres" {
  name  = "${var.project_name}-postgres"
  image = docker_image.postgres.image_id

  env = [
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
    "POSTGRES_DB=${var.postgres_db}"
  ]

  volumes {
    volume_name    = var.postgres_data_name
    container_path = "/var/lib/postgresql"
  }

  networks_advanced {
    name = var.postgres_network_name
  }

  healthcheck {
    test         = ["CMD", "pg_isready", "-U", var.postgres_user, "-d", var.postgres_db]
    interval     = "10s"
    timeout      = "5s"
    retries      = 5
    start_period = "30s"
  }

  restart = "unless-stopped"
}

resource "docker_image" "pgadmin" {
  name         = "dpage/pgadmin4"
  keep_locally = true
}

resource "docker_container" "pgadmin" {
  name  = "${var.project_name}-pgadmin"
  image = docker_image.pgadmin.image_id

  env = [
    "PGADMIN_DEFAULT_EMAIL=${var.pgadmin_user}",
    "PGADMIN_DEFAULT_PASSWORD=${var.pgadmin_password}"
  ]

  volumes {
    volume_name    = var.pgadmin_data_name
    container_path = "/var/lib/pgadmin"
  }

  ports {
    internal = 80
    external = var.pgadmin_port
  }

  networks_advanced {
    name = var.postgres_network_name
  }

  depends_on = [docker_container.postgres]
  restart    = "unless-stopped"
}