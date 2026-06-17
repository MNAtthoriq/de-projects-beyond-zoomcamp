# Module 1.A: Containerization as Code

![Status](https://img.shields.io/badge/Status-Completed-green)

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)

## Overview

Ingest multiple NY Taxi datasets (yellow taxi, green taxi, and zones) into a PostgreSQL database that can accessed using PgAdmin. The process is containerized using Docker.

What I improve from [original tutorial:](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/docker-sql)
|                  Original                  |                                My Version                                |
| :---------------------------------------------: | :-------------------------------------------------------------------: |
| `docker-compose` only runs postgres and pgadmin |         Entire pipeline runs in a single `docker compose up`          |
|       Re-running overwrites data silently       |    Safe re-runs by default, opt-in overwrite via `--force_replace`    |
|       Only ingest 1 dataset (yellow taxi)       | Ingest 3 datasets (yellow taxi, green taxi, and zones) simultaneously |
|             No parameter validation             |         Validates year/month range with clear error messages          |
|                   No logging                    |           Timestamped logging for full pipeline visibility            |

## Key Learnings

|        Concept         | What I Learned                                                                                                                                                                                                                                             |
| :--------------------: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|    Path resolution     | Path resolution follows the caller, not the runner. Example: `context:` block in `docker-compose.yaml` resolves from the compose file's location, while `docker build -t name:tag build_context` for `Dockerfile` resolves from wherever your terminal is. |
| Click + Docker Compose | `docker compose up` can't pass CLI flags hence use `envvar=` in `@click.option()` so your script reads from environment variables instead, making it fully compatible with Compose's `environment:` block.                                                 |
|  Inconsistent Pandas   | Pandas is inconsistent with missing columns. `dtype` silently ignores keys that don't match, but `parse_dates` raises a ValueError. Always validate columns exist before passing to `parse_dates`.                                                         |

## Structure

```
01-docker-terraform/docker/
├── ingest_data.py      ← ingestion script
├── Dockerfile          ← containerizes the ingestion script
├── docker-compose.yml  ← orchestrates postgres, pgadmin, ingestion script
└── README.md
```

## Usage

### 1. Start all services

```bash
docker compose up -d
```

### 2. Ingest data

```bash
docker compose run --rm ingest_data --year=2020 --month=6
```

### 3. Access pgAdmin

Open http://localhost:8085 in your browser.

| Field    | Value           |
| -------- | --------------- |
| Email    | admin@admin.com |
| Password | root            |

#### Register Server in pgAdmin

| Field    | Value   |
| -------- | ------- |
| Database | ny_taxi |
| Host     | pgdb    |
| Port     | 5432    |
| Username | root    |
| Password | root    |

## Environment Variables

| Variable      | CLI Option      | Default   | Description                                         |
| ------------- | --------------- | --------- | --------------------------------------------------- |
| PG_USER       | --pg_user       | root      | PostgreSQL username                                 |
| PG_PASS       | --pg_pass       | root      | PostgreSQL password                                 |
| PG_HOST       | --pg_host       | localhost | PostgreSQL host                                     |
| PG_PORT       | --pg_port       | 5432      | PostgreSQL port                                     |
| PG_DB         | --pg_db         | ny_taxi   | PostgreSQL database name                            |
| YEAR          | --year          | 2020      | Year of taxi data to ingest (2019-2021)             |
| MONTH         | --month         | 6         | Month of taxi data to ingest (1-12, max 7 for 2021) |
| CHUNKSIZE     | --chunksize     | 100000    | Number of rows to read per chunk                    |
| FORCE_REPLACE | --force_replace | False     | Force overwrite of existing table                   |