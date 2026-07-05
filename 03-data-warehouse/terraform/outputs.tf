output "bucket_name" {
  value = google_storage_bucket.benchmark_lake.name
}

output "dataset_id" {
  value = google_bigquery_dataset.benchmark.dataset_id
}

output "project_id" {
  value = var.project_id
}