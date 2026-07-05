variable "project_id" {
  description = "Your GCP project ID. Must already exist with billing enabled."
  type = string
}

variable "region" {
  description = "GCP region for GCS bucket and BiqQuery database."
  type = string
  default = "asia-southeast1"
}

variable "bucket_name" {
  description = "Globally unique name for GCS bucket (not just in this project, but ALL projects)."
  type = string
}

variable "dataset_id" {
  description = "BigQuery dataset name."
  type = string
}

variable "raw_data_retention_days" {
  description = "Days to keep raw data files in GCS before auto-deleted."
  type = number
  default = 7
}