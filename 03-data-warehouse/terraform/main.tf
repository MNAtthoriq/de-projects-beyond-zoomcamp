terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_project_service" "required" {
  for_each = toset([
    "bigquery.googleapis.com",
    "storage.googleapis.com",
  ])
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

resource "google_storage_bucket" "benchmark_lake" {
  project = var.project_id
  location = var.region
  name = var.bucket_name
  uniform_bucket_level_access = true
  # since it is for learning purpose, it will remove bucket when `terraform destroy`
  force_destroy = true

  lifecycle_rule {
    condition {
      age = var.raw_data_retention_days
    }
    action {
      type = "Delete"
    }
  }

  depends_on = [ google_project_service.required ]
}

resource "google_bigquery_dataset" "benchmark" {
  project                    = var.project_id
  location                   = var.region
  dataset_id                 = var.dataset_id
  delete_contents_on_destroy = true

  depends_on = [google_project_service.required]
}
