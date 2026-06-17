# Learning Data Engineering - Zoomcamp 2026
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

Personal learning repository for [Data Engineering Zoomcamp 2026](https://github.com/DataTalksClub/data-engineering-zoomcamp) by DataTalksClub. This repository documents my learning journey through the Zoomcamp. Each module contains working code I wrote myself, problems I encountered, and how I solved them.

```
LEARN   → Watch the lecture and take handwritten notes
CLOSE   → Stop passively following step-by-step tutorial
BUILD   → Coding from scratch without looking back
EXPLORE → Break, extend, and review intentionally
PUSH    → Commit my own code to this repository
```

## Progress
 
| Module     | Topic                    | Status        |
| ---------- | ------------------------ | ------------- |
| Module 1.A | Containerization as Code | 💚 Completed   |
| Module 1.B | Infrastructure as Code   | 💚 Completed   |
| Module 2   | Workflow Orchestration   | 🟡 In Progress |
| Workshop   | Data Ingestion           | ⬜ Upcoming    |
| Module 3   | Data Warehousing         | ⬜ Upcoming    |
| Module 4   | Analytics Engineering    | ⬜ Upcoming    |
| Module 5   | Data Platforms           | ⬜ Upcoming    |
| Module 6   | Batch Processing         | ⬜ Upcoming    |
| Module 7   | Streaming                | ⬜ Upcoming    |

## Repository Structure
 
```
learn-data-engineering-zoomcamp/
├── 01-docker-terraform/        ← completed
├── 02-workflow-orchestration/  ← (in progress)
├── workshop-data-ingestion/    ← coming soon
├── 03-data-warehouse/          ← coming soon
├── 04-analytics-engineering/   ← coming soon
├── 05-data-platforms/          ← coming soon
├── 06-batch/                   ← coming soon
├── 07-streaming/               ← coming soon
├── homework/                   ← (in progress)
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
 
# Run any script
uv run 01-docker-terraform/docker/ingest_data.py
```

> Every modules have their own README.md to tell about their usage setup.

## References

- Data Engineering Zoomcamp: https://github.com/DataTalksClub/data-engineering-zoomcamp
- DataTalks.Club: https://datatalks.club/
