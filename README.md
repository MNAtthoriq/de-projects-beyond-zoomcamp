# **Beyond Zoomcamp**: Data Engineering Portfolio

![Status](https://img.shields.io/badge/Status-In_Progress-yellow)

This portfolio demonstrates how I build reliable data pipelines,
reproducible infrastructure, cloud data platforms, and decision-support
applications using real-world datasets.

## Featured Projects

### **1. BigQuery Cost Optimization Simulator**

**Problem:** Data teams cannot easily estimate whether partitioning and clustering will materially reduce query costs for their workload.

**Solution:** Benchmarked multiple table configurations and built a predictive application that estimates bytes processed and query cost.

**Evidence:**
- 24,048 benchmark queries
- 48 BigQuery table configurations
- XGBoost Model with 99.98% R² and 1.6 MB MAE on test data
- Interactive Streamlit application

[Live Application](https://bigquery-partition-cluster-savings.streamlit.app/) · [View Project](/03-data-warehouse/README.md)

### **2. Reliable NYC Taxi Data Platform**

**Problem:** Recurring public-data ingestion requires repetitive manual work and can fail silently, create duplicate records, or break when the source schema changes.

**Solution:** Built an automated monthly data pipeline with orchestration, idempotent loading, data-quality gates, retries, schema-evolution handling, centralized Gmail failure alerts, and an operational monitoring dashboard.

**Evidence:**
- Automated ingestion, validation, and monitoring of monthly taxi data
- Ingested 11.31 million rows from 6 source files
- Detected and categorized 72,392 data-quality anomaly flags
- Interactive monitoring by filename, taxi type, and load date
- Automated Gmail alerts for pipeline failures
- Duplicate-safe reruns and schema-evolution handling

[Live Dashboard](https://datastudio.google.com/reporting/8bfe46b6-7e23-4628-9b3f-464be80dda8c) · [View Project](/02-workflow-orchestration/README.md)

## Project Portfolio

| Project | Problem Solved | Output | Zoomcamp Module |
|---|---|---|---|
| [BigQuery Cost Optimization Simulator](/03-data-warehouse/README.md) | Estimates the value of partitioning and clustering for different BigQuery workloads | [Live Simulator](https://bigquery-partition-cluster-savings.streamlit.app/) | Data Warehousing |
| [Reliable NYC Taxi Data Platform](/02-workflow-orchestration/README.md) | Automates reliable recurring ingestion with quality controls and failure monitoring | [Live Dashboard](https://datastudio.google.com/reporting/8bfe46b6-7e23-4628-9b3f-464be80dda8c) | Workflow Orchestration |
| [Containerized Local Data Platform](/01-docker-terraform) | Creates a reproducible local PostgreSQL environment instead of relying on manual setup | Code and technical demonstration | Containerization & Infrastructure |

## Why “Beyond Zoomcamp”?

I use the
[Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)
curriculum by [DataTalks.Club](https://datatalks.club/) as a structured foundation for learning data engineering.

For each module, instead of blindly copy-pasting completed code, I close the tutorial and rebuild the project. My goals is not to reproduce same lecture code, but to compose a better version of my own.

> **LEARN**   → Learn the concepts
>
> **CLOSE**   → Close the tutorial  
>
> **BUILD**   → Build better projects

## About Me

**Muhammad Naufal At-Thoriq**

I am an Operations Analyst with two years of experience using data,
automation, and dashboards to improve operational workflows and decision-making.

My professional work includes Python automation, reusable data-processing
pipelines, operational reporting, data validation, and dashboard development.

I am now expanding that experience into cloud data engineering, orchestration,
data warehousing, and analytics engineering.

[GitHub](https://github.com/MNAtthoriq) · [LinkedIn](https://linkedin.com/in/mnatthoriq)