# BEYOND ZOOMCAMP: Data Engineering Projects Collection 
![Status](https://img.shields.io/badge/Status-In_Progress-yellow)
<!--
![Status](https://img.shields.io/badge/Status-Completed-green)
-->

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?logo=terraform&logoColor=white)
<!--
![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?logo=googlecloud&logoColor=white)
![BigQuery](https://img.shields.io/badge/BigQuery-669DF6?logo=googlebigquery&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?logo=duckdb&logoColor=black)
![Apache Spark](https://img.shields.io/badge/Apache_Spark-E25A1C?logo=apachespark&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Apache_Kafka-231F20?logo=apachekafka&logoColor=white)
-->

This repository is a growing collection of Data Engineering projects. It is `not` a compilation of lecture notes. 

I am using [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) curriculum as a foundation. For each module, instead of blindly copy-pasting completed code, I close the tutorial and rebuild the project. My goals is not to reproduce same lecture code, but to compose a better version of my own.

I push it beyond tutorial. Beyond Zoomcamp.

```
LEARN  → Learn the concepts
CLOSE  → Close the tutorial
BUILD  → Build better projects
```

## Progress

| Module | Project | Status | Stack |
|---|---|:---:|:---:|
| 1.A - Containerization | [Taxi Data Ingestion Pipeline](01-docker-terraform/docker/) | 🟢 | <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white"> <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white"><br><img src="https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white"> |
| 1.B - Infrastructure as Code | [Containerized Data Platform Infrastructure](01-docker-terraform/terraform/) | 🟢 | <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white"> <img src="https://img.shields.io/badge/Terraform-844FBA?logo=terraform&logoColor=white"><br><img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white"> <img src="https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white"> |
| 2 - Workflow Orchestration | — | 🟡 | — |
| 3 - Data Warehousing | — | ⚪️ | — |
| 4 - Analytics Engineering | — | ⚪️ | — |
| 5 - Data Platforms | — | ⚪️ | — |
| 6 - Batch Processing | — | ⚪️ | — |
| 7 - Streaming | — | ⚪️ | — |
| Data Ingestion Workshop | — | ⚪️ | — |

`Status = 🟢 Done | 🟡 Progress | ⚪️ Upcoming`

## Repository Structure
 
```
learn-data-engineering-zoomcamp/
├── 01-docker-terraform/        ← completed
├── 02-workflow-orchestration/  ← (in progress)
├── 03-data-warehouse/          ← coming soon
├── 04-analytics-engineering/   ← coming soon
├── 05-data-platforms/          ← coming soon
├── 06-batch/                   ← coming soon
├── 07-streaming/               ← coming soon
├── workshop-data-ingestion/    ← coming soon
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
├── LICENSE
└── README.md
```

## Setup
 
This repo uses [uv](https://github.com/astral-sh/uv) for Python environment management.
 
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/data-engineering-zoomcamp.git
cd learn-data-engineering-zoomcamp
 
# Install dependencies
uv sync --locked
```

> Each project's README has its own run instructions.

## References

- Data Engineering Zoomcamp: https://github.com/DataTalksClub/data-engineering-zoomcamp
- DataTalks.Club: https://datatalks.club/
