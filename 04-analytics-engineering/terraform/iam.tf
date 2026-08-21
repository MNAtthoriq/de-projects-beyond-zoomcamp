resource "google_service_account" "pipeline" {
  account_id   = "eia-analytics-pipeline"
  display_name = "EIA Analytics Pipeline"
  project      = var.project_id

  depends_on = [google_project_service.required]
}

resource "google_project_iam_member" "pipeline_bigquery_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.pipeline.email}"
}