# Module 1.B: Infrastructure as Code

![Status](https://img.shields.io/badge/Status-Completed-green)

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-844FBA?logo=terraform&logoColor=white)

## Overview

Local database infrastructure provisioned with Terraform for reproducible, version-controlled, and teardown-safe. 
It using Docker provider with PostgreSQL and pgAdmin images.

What I improve from [original tutorial:](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/terraform)
|            Original             |                                     My Version                                     |
| :-----------------------------: | :--------------------------------------------------------------------------------: |
|          No `modules`           |      Modularized into lifecycle-based modules (networks, storages, services)       |
|          No `outputs`           | Added `outputs` for pgAdmin access info (like url and register server information) |
| Variables hardcoded as defaults |               Externalized via `.tfvars` for flexible configuration                |
| No sensitive variable handling  |                        Sensitive variables properly handled                        |

> **Note:** This project uses local Docker infrastructure instead of GCP due to billing setup issues (on process apply credit card).
> The concepts are provider-agnostic and transfer directly to cloud providers like GCP, AWS, or Azure.

## Key Learnings

|            Concept            | What I Learned                                                                                                                                                |
| :---------------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Variables, Outputs, & Modules | Root `main.tf` acts as the middleman: passing variables into modules and receiving their `outputs.tf` values to wire modules together                         |
|           Debugging           | `terraform init` and `terraform plan` catch errors early before any infrastructure is touched                                                                 |
|       Destroy Behaviour       | Terraform destroys everything it manages after `terraform destroy` including pre-existing resources it adopted. Be cautious with persistent data like volumes |

## Structure

```
01-docker-terraform/terraform/
├── main.tf
├── outputs.tf
├── variables.tf
├── .terraform.lock.hcl       ← for reproducibility
├── terraform.tfvars.example  ← copy into terraform.tfvars for variable input
├── modules/                  ← categorize by life-cycle for easier re-install
│   ├── networks/             ← docker-network, rarely changes
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   └── variables.tf
│   ├── storages/             ← docker-volume, seldom changes
│   │   ├── main.tf
│   │   ├── outputs.tf
│   │   └── variables.tf
│   └── services/             ← docker-image and docker-container, often changes
│       ├── main.tf
│       └── variables.tf
└── README.md
```

## Usage

### 1. Set up variables
```bash
cp terraform.tfvars.example terraform.tfvars
```
Edit `terraform.tfvars` with your values:
```hcl
project_name      = "learn-de-terraform"
postgres_user     = "root"
postgres_password = "root"
postgres_db       = "learn-de-terraform-postgres-db"
pgadmin_user      = "admin@admin.com"
pgadmin_password  = "root"
pgadmin_port      = 8010
```

### 2. Initialize Terraform
```bash
terraform init
```

---

### 3. Deploy Terraform
#### A. Deploy All
```bash
terraform apply
```

After apply, Terraform will output:
- pgAdmin URL → `http://localhost:<pgadmin_port>`
- PostgreSQL connection details (host, port, user, db name)

Use the PostgreSQL connection details to register the server in pgAdmin.

#### B. Deploy by Lifecycle
Each module is categorized by how often it changes, so you can redeploy only what you need without touching stable infrastructure.

```bash
terraform apply -target=module.networks   # once, rarely changes
terraform apply -target=module.storages   # once, seldom changes
terraform apply -target=module.services   # as needed, often changes
```

> Always provision `networks` → `storages` → `services` in order. Services depend on both.

### 4. Teardown Terraform
```bash
# Remove services only — keeps volumes and network intact, your data is safe
terraform destroy -target=module.services

# Remove everything
terraform destroy
```

> `terraform destroy` without `-target` will destroy volumes and all stored data.

## Environment Variables

| Variable            | Description                     | Example                 | Sensitive |
| ------------------- | ------------------------------- | ----------------------- | :-------: |
| `project_name`      | Prefix for all Docker resources | `learn-de-terraform`    |    No     |
| `postgres_user`     | PostgreSQL username             | `root`                  |    No     |
| `postgres_password` | PostgreSQL password             | `root`                  |    Yes    |
| `postgres_db`       | PostgreSQL database name        | `learn-de-terraform-db` |    No     |
| `pgadmin_user`      | pgAdmin login email             | `admin@admin.com`       |    No     |
| `pgadmin_password`  | pgAdmin login password          | `root`                  |    Yes    |
| `pgadmin_port`      | Host port exposed for pgAdmin   | `8010`                  |    No     |