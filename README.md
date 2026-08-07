# **Beyond Zoomcamp**: Data Engineering Portfolio

![Status](https://img.shields.io/badge/Status-In_Progress-yellow)

This portfolio demonstrates how I build reliable data pipelines,
reproducible infrastructure, cloud data platforms, and decision-support
applications using real-world datasets.

## Featured Projects

### **1. BigQuery Cost Optimization Simulator**

[Live Application](https://bigquery-partition-cluster-savings.streamlit.app/) · [View Project](/03-data-warehouse/README.md)

**Problem:** Data teams cannot easily estimate whether partitioning and clustering will materially reduce query costs for their workload.

**Solution:** Benchmarked multiple table configurations and built a predictive application that estimates bytes processed and query cost.

| Metric | Result |
|---|---:|
| Benchmark Queries | 24,048 BigQuery dry-run queries |
| Table Configurations | 48 benchmark tables |
| Largest Data Tier | 48.51 million rows / 7.23 GB |
| Model Test Performance | R² 0.9998 / MAE 1.60 MB |

### **2. Reliable NYC Taxi Data Platform**

[Live Dashboard](https://datastudio.google.com/reporting/8bfe46b6-7e23-4628-9b3f-464be80dda8c) · [View Project](/02-workflow-orchestration/README.md)

**Problem:** Monthly taxi data needs to be downloaded, checked, and loaded repeatedly. This process can fail, create duplicate data, or break when the source changes.

**Solution:** Built an automated pipeline that downloads new data, validates it, safely updates BigQuery, handles expected source changes, sends Gmail alerts when a run fails, and updates a monitoring dashboard.

| Metric | Result |
|---|---:|
| Pipeline Execution | 3 months of data processed with 0 failed runs |
| Rows Ingested | 11.31 million rows |
| Data Anomaly Flags Detected | 72,392 anomalies |
| Files Ingested | 6 files |

## Project Portfolio

| Project | Output | Problem Solved | Zoomcamp Module |
|---|---|---|---|
| [BigQuery Cost Optimization Simulator](/03-data-warehouse/README.md) | [Live Simulator](https://bigquery-partition-cluster-savings.streamlit.app/) | Estimates the value of partitioning and clustering for different BigQuery workloads | Data Warehousing |
| [Reliable NYC Taxi Data Platform](/02-workflow-orchestration/README.md) | [Live Dashboard](https://datastudio.google.com/reporting/8bfe46b6-7e23-4628-9b3f-464be80dda8c) | Automates reliable recurring ingestion with quality controls and failure monitoring | Workflow Orchestration |
| [Containerized Local Data Platform](/01-docker-terraform) | Code and technical demonstration | Creates a reproducible local PostgreSQL environment instead of relying on manual setup | Containerization & Infrastructure |

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