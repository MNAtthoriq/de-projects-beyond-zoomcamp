# Orchestrated Taxi Data Pipeline

![Status](https://img.shields.io/badge/Status-Completed-green)
![Module](https://img.shields.io/badge/Module%202-Workflow%20Orchestration-blue)

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?logo=terraform&logoColor=white)
![Kestra](https://img.shields.io/badge/Kestra-5A3FF2?style=flat&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIGlkPSJMYXllcl8xIiB4PSIwIiB5PSIwIiB2ZXJzaW9uPSIxLjEiIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj48c3R5bGU%2BLnN0MHtmaWxsOiNhOTUwZmZ9LnN0MntmaWxsOiNjZDg4ZmZ9PC9zdHlsZT48cGF0aCBkPSJNMjM3LjkgMTk3LjJjMTAtMTAgMjYuMi0xMCAzNi4yIDBsNDEuMSA0MS4xYzEwIDEwIDEwIDI2LjIgMCAzNi4ybC00MS4xIDQxLjFjLTEwIDEwLTI2LjIgMTAtMzYuMiAwbC00MS4xLTQxLjFjLTEwLTEwLTEwLTI2LjIgMC0zNi4yem0xODkuNC0uM2M5LjgtOS44IDI1LjgtOS44IDM1LjYgMGw0MS44IDQxLjhjOS44IDkuOCA5LjggMjUuOCAwIDM1LjZMNDYyLjkgMzE2Yy05LjggOS44LTI1LjggOS44LTM1LjYgMGwtNDEuOC00MS44Yy05LjgtOS44LTkuOC0yNS44IDAtMzUuNnM0MS44LTQxLjcgNDEuOC00MS43IiBjbGFzcz0ic3QwIi8%2BPHBhdGggZD0iTTIzOC4yIDcuOEMyNDgtMiAyNjQtMiAyNzMuOCA3LjhsNDEuOCA0MS44YzkuOCA5LjggOS44IDI1LjggMCAzNS42TDI3My44IDEyN2MtOS44IDkuOC0yNS44IDkuOC0zNS42IDBsLTQxLjgtNDEuOGMtOS44LTkuOC05LjgtMjUuOCAwLTM1LjZ6IiBzdHlsZT0iZmlsbDojZTljMWZmIi8%2BPHBhdGggZD0iTTIyMC43IDE0My44YzEwIDEwIDEwIDI2LjIgMCAzNi4ybC00MS4xIDQxLjFjLTEwIDEwLTI2LjIgMTAtMzYuMiAwTDEwMi4yIDE4MGMtMTAtMTAtMTAtMjYuMiAwLTM2LjJsNDEuMS00MS4xYzEwLTEwIDI2LjItMTAgMzYuMiAweiIgY2xhc3M9InN0MiIvPjxwYXRoIGQ9Ik0xMjYuNSAyMzguNmM5LjggOS44IDkuOCAyNS44IDAgMzUuNkw4NC43IDMxNmMtOS44IDkuOC0yNS44IDkuOC0zNS42IDBMNy40IDI3NC4yYy05LjgtOS44LTkuOC0yNS44IDAtMzUuNmw0MS44LTQxLjhjOS44LTkuOCAyNS44LTkuOCAzNS42IDB6IiBjbGFzcz0ic3QwIi8%2BPHBhdGggZD0iTTQwOS44IDE0My44YzEwIDEwIDEwIDI2LjIgMCAzNi4ybC00MS4xIDQxLjFjLTEwIDEwLTI2LjIgMTAtMzYuMiAwTDI5MS4zIDE4MGMtMTAtMTAtMTAtMjYuMiAwLTM2LjJsNDEuMS00MS4xYzEwLTEwIDI2LjItMTAgMzYuMiAweiIgY2xhc3M9InN0MiIvPjxwYXRoIGQ9Ik0yOTYuNSA0MTMuOWMyMi4zIDIyLjMgMjIuMyA1OC42IDAgODAuOS0yMi40IDIyLjMtNTguNiAyMi4zLTgwLjkgMC0yMi40LTIyLjQtMjIuNC01OC42IDAtODAuOSAyMi4zLTIyLjQgNTguNS0yMi40IDgwLjkgMCIgc3R5bGU9ImZpbGw6I2Y2MmU3NiIvPjwvc3ZnPg%3D%3D&logoWidth=20)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?logo=googlecloud&logoColor=white)
![Google BigQuery](https://img.shields.io/badge/Google_BigQuery-669DF6?logo=googlebigquery&logoColor=white)
![Google Data Studio](https://img.shields.io/badge/Google_Data_Studio-4285F4?logo=looker&logoColor=white)

## Overview

A monthly ELT pipeline that pulls NYC TLC taxi trip and zone data into BigQuery, orchestrated end-to-end with [Kestra](https://kestra.io) and provisioned on GCP with Terraform. It deduplicates, quality-gates, schema-evolves, and alerts on failure, then feeds a Google Data Studio (formerly Looker Studio) proof for monitoring.

What I improve from the [original tutorial](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/02-workflow-orchestration):
| Original tutorial | My Version |
| :--- | :--- |
| Static, gzipped **CSV** backup from GitHub as source data | Live monthly **Parquet** release straight from NYC TLC's official CDN as source data |
| No **retries**, no data **quality check**, no **alerting** | Task **retries**, a SQL **data-quality gate**, and centralized **Gmail alert** flow for the whole project |
| No **schema evolution** handling | Using `ALTER TABLE ...` to absorbs TLC's **new `cbd_congestion_fee` column** (introduced in 2025) without breaking the pipeline |
| Keeps external and staging tables after loading | Drops external and staging tables after use to reduce storage costs and keep the dataset clean |
| **Mixed** infrastructure and orchestration responsibilities (everything using Kestra) | Clear separation of concerns: **Terraform for infrastructure**, **Kestra for orchestration** |
| Flow **manually** copy-pasted into Kestra UI | Flows synced **automatically** using local sync |
| **Manual** secret configuration | Scripts **automate** Base64 encoding and `.env` import into Kestra's Key-Value Store |
| No **dimension data** or **monitoring proof** | Loads the NYC TLC **zone lookup table** and builds **monitoring views** for Google Data Studio **proof** |

## Key Learnings

| Concept | What I Learned |
| :---: | :--- |
| Idempotent Loads | MD5 hash of business keys as `unique_row_id`, combined with `MERGE`, means rerunning or backfilling a month never creates duplicate rows |
| Data Quality Gates | SQL `ERROR()` checks fail a run immediately on 0 rows or duplicate keys, instead of letting bad data flow downstream silently |
| Schema Evolution | `ALTER TABLE ... ADD COLUMN IF NOT EXISTS` lets the pipeline absorb new source columns without a manual migration |
| Pebble Syntax | Pebble does not support nested expressions, so variables should be declared explicitly before use |
| Kestra's Trigger | Trigger may not start if concurrency is limited. Re-create trigger solve this problem |

## Proof

<p align="center">
  <img src="proof/proof.gif" width="500" alt="Dashboard demo — filtering and drill-down">
</p>

<p align="center">
  <a href="https://datastudio.google.com/reporting/8bfe46b6-7e23-4628-9b3f-464be80dda8c">
    View the interactive Google Data Studio dashboard here
  </a>
</p>

## Structure

```
02-workflow-orchestration/
├── docker-compose.yml          ← Docker Compose configuration for Kestra
├── .env.example
├── .env.secrets.example
├── flows/                      ← orchestration flow by Kestra
│   ├── main_zoomcamp.00_environment_setup.yaml
│   ├── main_zoomcamp.01_taxi_tripdata_pipeline.yaml
│   ├── main_zoomcamp.02_taxi_zone_pipeline.yaml
│   ├── main_zoomcamp.03_proof_views_pipeline.yaml
│   └── main_zoomcamp.99_monitoring_alerts.yaml
├── scripts/
│   ├── bootstrap_env.sh        ← pushes terraform output into Kestra KV
│   └── encode_secrets.sh       ← encodes .env.secrets into .env_encoded
├── terraform/                  ← provisions GCS bucket, BigQuery dataset, service account
│   ├── main.tf
│   ├── outputs.tf
│   ├── variables.tf
│   └── terraform.tfvars.example
├── proof/                      ← proof and gif as proof that project completed
│   ├── proof_export.pdf
│   └── proof.gif
└── README.md
```

## Usage

### Prerequisites
- Docker
- Terraform >= 1.5
- A GCP project with billing enabled, and credentials available (`gcloud auth application-default login`)
- `jq` and `curl` (used by `scripts/bootstrap_env.sh`)
- *(Optional)* a Gmail account + [App Password](https://support.google.com/mail/answer/185833) for `flows/99_monitoring_alerts.yaml`

### 1. Provision infrastructure
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars   # fill in project_id, bucket_name, etc.
terraform init
terraform apply
```

### 2. Configure environment
```bash
cd ..
cp .env.example .env                      # fill for Kestra's Key-Value Store
cp .env.secrets.example .env.secrets      # fill for Kestra's Secret
```

### 3. Encode secrets for Kestra
```bash
./scripts/encode_secrets.sh   # encoding .env.secrets into base64 as .env_encoded
```

### 4. Start Kestra
```bash
docker compose up -d
```
Kestra UI → `http://localhost:${KESTRA_UI_PORT:-18081}` (login from `.env`)

### 5. Bootstrap the KV store
```bash
./scripts/bootstrap_env.sh   # pushes terraform output → Kestra KV, once per environment
```

### 6. Run the pipelines
Trigger manually from the Kestra UI, or let the schedules run on the 5th of every month:
- `02_taxi_zone_pipeline` → 08:00 UTC
- `01_taxi_tripdata_pipeline` (green) → 09:00 UTC
- `01_taxi_tripdata_pipeline` (yellow) → 10:00 UTC
- `03_dashboard_views_pipeline` fires automatically once both succeed, time window 08:00 - 12:00 UTC

### Teardown
```bash
docker compose down -v              # stop Kestra + Postgres, remove local volumes
cd terraform && terraform destroy   # remove GCS bucket, BigQuery dataset, service account
```

## Environment Variables

| Variable | File | Description | Sensitive |
| :--- | :--- | :--- | :---: |
| `KESTRA_POSTGRES_PASSWORD` | `.env` | Password for Kestra's internal Postgres metastore | Yes |
| `KESTRA_BASIC_AUTH_USERNAME` | `.env` | Username to log into the Kestra UI | No |
| `KESTRA_BASIC_AUTH_PASSWORD` | `.env` | Password to log into the Kestra UI | Yes |
| `KESTRA_UI_PORT` | `.env` | Host port for Kestra UI (default `18081`) | No |
| `GCP_CREDS_BASE64` | `.env.secrets` | Base64 service-account key, from `terraform output -raw kestra_service_account_key_base64` | Yes |
| `GMAIL_ADDRESS` | `.env.secrets` | Sender/receiver address for failure alerts (optional) | No |
| `GMAIL_APP_PASSWORD` | `.env.secrets` | Gmail App Password for SMTP auth (optional) | Yes |
| `project_id` | `terraform.tfvars` | Google Cloud project ID where resources will be created | No |
| `region` | `terraform.tfvars` | Google Cloud region for provisioning resources | No |
| `bucket_name` | `terraform.tfvars` | Name of the GCS bucket used for raw data storage | No |
| `dataset_id` | `terraform.tfvars` | BigQuery dataset name for the ELT pipeline | No |
| `service_account_id` | `terraform.tfvars` | ID of the service account created for Kestra | No |
| `raw_data_retention_days` | `terraform.tfvars` | Number of days to retain raw data in the GCS bucket before automatic deletion | No |

## Author

**Muhammad Naufal At-Thoriq**
- GitHub: [MNAtthoriq](https://github.com/MNAtthoriq)
- LinkedIn: [Muhammad Naufal At-Thoriq](https://linkedin.com/in/mnatthoriq)

## Reference

- [DE Projects - Beyond Zoomcamp](../)
- [Module 2 - Workflow Orchestration (original tutorial)](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/02-workflow-orchestration)
- [Kestra Documentation](https://kestra.io/docs)
- [Terraform - Google Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)