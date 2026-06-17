terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 4.2.0"
    }
  }
}

provider "docker" {}

module "networks" {
  source       = "./modules/networks"
  project_name = var.project_name
}

module "storages" {
  source       = "./modules/storages"
  project_name = var.project_name
}

module "services" {
  source                = "./modules/services"
  project_name          = var.project_name
  postgres_network_name = module.networks.postgres_network_name
  postgres_data_name    = module.storages.postgres_data_name
  pgadmin_data_name     = module.storages.pgadmin_data_name
  postgres_user         = var.postgres_user
  postgres_password     = var.postgres_password
  postgres_db           = var.postgres_db
  pgadmin_user          = var.pgadmin_user
  pgadmin_password      = var.pgadmin_password
  pgadmin_port          = var.pgadmin_port
}