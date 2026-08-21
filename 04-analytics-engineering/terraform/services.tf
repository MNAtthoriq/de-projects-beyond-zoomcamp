locals {
  require_services = [
    "bigquery.googleapis.com",
    "storage.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
  ]
}

resource "google_project_service" "required" {
  for_each           = toset(local.require_services)
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}