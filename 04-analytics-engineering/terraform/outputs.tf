output "pipeline_service_account_email" {
  description = "Service account used by the EIA analytics pipeline"
  value       = google_service_account.pipeline.email
}