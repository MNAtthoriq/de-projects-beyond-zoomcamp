# Reliable NYC Taxi Data Platform

![Status](https://img.shields.io/badge/Status-Completed-green)

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?logo=terraform&logoColor=white)
![Kestra](https://img.shields.io/badge/Kestra-5A3FF2?style=flat&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIGlkPSJMYXllcl8xIiB4PSIwIiB5PSIwIiB2ZXJzaW9uPSIxLjEiIHZpZXdCb3g9IjAgMCA1MTIgNTEyIj48c3R5bGU%2BLnN0MHtmaWxsOiNhOTUwZmZ9LnN0MntmaWxsOiNjZDg4ZmZ9PC9zdHlsZT48cGF0aCBkPSJNMjM3LjkgMTk3LjJjMTAtMTAgMjYuMi0xMCAzNi4yIDBsNDEuMSA0MS4xYzEwIDEwIDEwIDI2LjIgMCAzNi4ybC00MS4xIDQxLjFjLTEwIDEwLTI2LjIgMTAtMzYuMiAwbC00MS4xLTQxLjFjLTEwLTEwLTEwLTI2LjIgMC0zNi4yem0xODkuNC0uM2M5LjgtOS44IDI1LjgtOS44IDM1LjYgMGw0MS44IDQxLjhjOS44IDkuOCA5LjggMjUuOCAwIDM1LjZMNDYyLjkgMzE2Yy05LjggOS44LTI1LjggOS44LTM1LjYgMGwtNDEuOC00MS44Yy05LjgtOS44LTkuOC0yNS44IDAtMzUuNnM0MS44LTQxLjcgNDEuOC00MS43IiBjbGFzcz0ic3QwIi8%2BPHBhdGggZD0iTTIzOC4yIDcuOEMyNDgtMiAyNjQtMiAyNzMuOCA3LjhsNDEuOCA0MS44YzkuOCA5LjggOS44IDI1LjggMCAzNS42TDI3My44IDEyN2MtOS44IDkuOC0yNS44IDkuOC0zNS42IDBsLTQxLjgtNDEuOGMtOS44LTkuOC05LjgtMjUuOCAwLTM1LjZ6IiBzdHlsZT0iZmlsbDojZTljMWZmIi8%2BPHBhdGggZD0iTTIyMC43IDE0My44YzEwIDEwIDEwIDI2LjIgMCAzNi4ybC00MS4xIDQxLjFjLTEwIDEwLTI2LjIgMTAtMzYuMiAwTDEwMi4yIDE4MGMtMTAtMTAtMTAtMjYuMiAwLTM2LjJsNDEuMS00MS4xYzEwLTEwIDI2LjItMTAgMzYuMiAweiIgY2xhc3M9InN0MiIvPjxwYXRoIGQ9Ik0xMjYuNSAyMzguNmM5LjggOS44IDkuOCAyNS44IDAgMzUuNkw4NC43IDMxNmMtOS44IDkuOC0yNS44IDkuOC0zNS42IDBMNy40IDI3NC4yYy05LjgtOS44LTkuOC0yNS44IDAtMzUuNmw0MS44LTQxLjhjOS44LTkuOCAyNS44LTkuOCAzNS42IDB6IiBjbGFzcz0ic3QwIi8%2BPHBhdGggZD0iTTQwOS44IDE0My44YzEwIDEwIDEwIDI2LjIgMCAzNi4ybC00MS4xIDQxLjFjLTEwIDEwLTI2LjIgMTAtMzYuMiAwTDI5MS4zIDE4MGMtMTAtMTAtMTAtMjYuMiAwLTM2LjJsNDEuMS00MS4xYzEwLTEwIDI2LjItMTAgMzYuMiAweiIgY2xhc3M9InN0MiIvPjxwYXRoIGQ9Ik0yOTYuNSA0MTMuOWMyMi4zIDIyLjMgMjIuMyA1OC42IDAgODAuOS0yMi40IDIyLjMtNTguNiAyMi4zLTgwLjkgMC0yMi40LTIyLjQtMjIuNC01OC42IDAtODAuOSAyMi4zLTIyLjQgNTguNS0yMi40IDgwLjkgMCIgc3R5bGU9ImZpbGw6I2Y2MmU3NiIvPjwvc3ZnPg%3D%3D&logoWidth=20)
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?logo=googlecloud&logoColor=white)
![Google BigQuery](https://img.shields.io/badge/Google_BigQuery-669DF6?logo=googlebigquery&logoColor=white)
![Google Data Studio](https://img.shields.io/badge/Google_Data_Studio-4285F4?logo=looker&logoColor=white)

An automated monthly data pipeline that collects NYC taxi data, checks its quality, loads it into BigQuery, alerts when something fails, and provides a dashboard to monitor the result.

[Live Dashboard](https://datastudio.google.com/reporting/8bfe46b6-7e23-4628-9b3f-464be80dda8c) · [Technical Documentation](TECHNICAL.md)

*This project is part of [Beyond Zoomcamp: Data Engineering Portfolio](https://github.com/MNAtthoriq/de-projects-beyond-zoomcamp/blob/main/README.md)*

## Executive Summary

<table>
  <tr>
    <td width="18%"><strong>Problem</strong></td>
    <td>Monthly taxi data needs to be downloaded, checked, and loaded repeatedly. This process can fail, create duplicate data, or break when the source changes.</td>
  </tr>
  <tr>
    <td width="18%"><strong>Why It Matters</strong></td>
    <td>If those problems go unnoticed, analysts may work with incomplete, duplicated, or outdated data. Manual checking also adds repetitive work every month.</td>
  </tr>
  <tr>
    <td width="18%"><strong>Solution</strong></td>
    <td>Built an automated pipeline that downloads new data, validates it, safely updates BigQuery, handles expected source changes, sends Gmail alerts when a run fails, and updates a monitoring dashboard.</td>
  </tr>
</table>

## Results

### Measured Metrics

| Metric | Result |
|---|---:|
| Pipeline Execution | 3 months of data processed with 0 failed runs |
| Rows Ingested | 11.31 million rows |
| Data Anomaly Flags Detected | 72,392 anomalies |
| Files Ingested | 6 files |

### Key Capabilities

- **Automated data pipeline** — collects, checks, and loads new NYC taxi data into BigQuery with minimal manual work
- **Safe data updates** — prevents duplicate records when the same data is processed again
- **Built-in data quality checks** — stops problematic loads and flags unusual records for investigation
- **Automatic failure handling** — retries temporary failures and sends Gmail alerts when a pipeline run has a problem
- **Interactive monitoring dashboard** — shows data loads, processing volume, and detected data-quality issues in one place

## Live Output

<p align="left">
  <img src="proof/proof.png" width="500" alt="Dashboard demo — filtering and drill-down">
</p>

[Open Live Dashboard here](https://datastudio.google.com/reporting/8bfe46b6-7e23-4628-9b3f-464be80dda8c)

The dashboard gives a quick view of whether the pipeline is working and what data was loaded.

Users can:

- See how many files and rows have been ingested
- Check the latest successful load
- Compare Yellow and Green taxi data volume
- See how many data-quality issues were flagged in each file
- Investigate issue types such as negative amounts, negative trip duration, and zero-fare trips
- Filter the dashboard by file, taxi type, and load date

> The 72,392 anomaly flags are rule-based checks that highlight records worth investigating. A flagged record is not automatically an invalid record.

## Architecture

```mermaid
flowchart LR
    A[NYC Taxi Data] --> B{Pipeline Run Successful?}
    B -->|Yes| C[BigQuery]
    C --> D[Monitoring Dashboard]
    B -->|No / Warning| E[Gmail Alert]
```

In simple terms:

1. New taxi data is collected automatically each month.
2. The pipeline checks the data before adding it to the main dataset.
3. Valid data is safely loaded into BigQuery.
4. If the process fails, an email alert is sent automatically.
5. The dashboard shows what was loaded and where potential data-quality issues exist.

## Technical Documentation

For detailed explanation about how the project is built, configured, and run:

[Read Technical Documentation here](TECHNICAL.md)

## About Me

**Muhammad Naufal At-Thoriq**

I am an Operations Analyst with two years of experience using data, automation, and dashboards to improve operational workflows and decision-making.

My professional work includes Python automation, reusable data-processing pipelines, operational reporting, data validation, and dashboard development.

I am expanding that experience into cloud data engineering, workflow orchestration, data warehousing, and analytics engineering.

[GitHub](https://github.com/MNAtthoriq) · [LinkedIn](https://linkedin.com/in/mnatthoriq)