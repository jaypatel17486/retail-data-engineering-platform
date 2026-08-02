# 🚀 Retail Data Engineering Platform

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-3.5-orange?style=for-the-badge&logo=apachespark)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-7.6-black?style=for-the-badge&logo=apachekafka)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.x-017CEE?style=for-the-badge&logo=apacheairflow)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)

</p>

---

## 📌 Overview

The **Retail Data Engineering Platform** is an end-to-end modern data engineering project that demonstrates how retail transaction data can be ingested, streamed, transformed, validated, stored in a dimensional data warehouse, and orchestrated using Apache Airflow.

This project simulates a production-grade retail analytics platform by combining real-time streaming with a warehouse architecture and ETL automation.

---

## 📚 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Data Flow](#-data-flow)
- [Data Warehouse](#-data-warehouse)
- [Airflow Pipeline](#-airflow-pipeline)
- [Data Quality](#-data-quality)
- [Audit Logging](#-audit-logging)
- [Docker Services](#-docker-services)
- [Getting Started](#-getting-started)
- [Future Improvements](#-future-improvements)

---

# 🏗 System Architecture

<p align="center">
    <img src="docs/architecture.drawio" width="100%">
</p>

The architecture follows a modern data engineering design where retail data is generated, streamed through Apache Kafka, processed using Apache Spark Structured Streaming, orchestrated with Apache Airflow, and stored in a PostgreSQL Star Schema data warehouse.

---

# 🚀 Features

- Real-time streaming using Apache Kafka
- Spark Structured Streaming pipeline
- PostgreSQL Landing Zone
- Star Schema Data Warehouse
- Apache Airflow orchestration
- Automated ETL pipeline
- Data Quality validation
- ETL Audit Logging
- Analytics Views
- Dockerized infrastructure
- Modular project architecture
- Production-style logging

---

# 🛠 Technology Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Database | PostgreSQL |
| Streaming | Apache Kafka |
| Processing | Apache Spark Structured Streaming |
| Orchestration | Apache Airflow |
| Containerization | Docker |
| Warehouse | PostgreSQL Star Schema |
| Logging | Python Logging |
| Version Control | Git + GitHub |

---

# 📂 Project Structure

```text
retail-data-engineering-platform/

airflow/
│
├── dags/
├── logs/
└── plugins/

dashboard/

docker/

docs/

logs/

quality/

scripts/

spark/

streaming/

tests/

utils/

warehouse/
│
├── loaders/
├── sql/
└── README.md

README.md

docker-compose.yml

requirements.txt
```

---

# 📊 Data Flow

```text
Retail Data Generator

↓

Apache Kafka

↓

Spark Structured Streaming

↓

Landing Table

streaming_orders

↓

Apache Airflow

↓

Warehouse ETL

↓

Dimension Tables

↓

Fact Table

↓

Analytics Views
```

---

# 📈 Data Warehouse

### Warehouse Schema

<p align="center">
    <img src="docs/warehouse star schema.md" width="100%">
</p>

### Fact Table

<p align="center">
    <img src="docs/fact table.png" width="100%">
</p>

---

# 🔄 ETL Workflow

```text
Landing Table

↓

Load Customer Dimension

↓

Load Product Dimension

↓

Load Date Dimension

↓

Load Fact Sales

↓

Refresh Analytics Views

↓

Audit Logging

↓

Complete
```

---

# 📋 Airflow Pipeline

<p align="center">
    <img src="docs/airflow retail_etl.png.png" width="100%">
</p>

The **retail_etl** DAG automates the warehouse refresh.

Pipeline:

```text
Start

↓

Load Dimensions

↓

Load Fact Sales

↓

Write Audit Log

↓

Finish
```

---

# ✅ Data Quality

The project validates:

- Missing Customer IDs
- Missing Product IDs
- Invalid Quantity
- Invalid Price
- Duplicate Orders

Invalid records can be captured for further analysis.

---

# 📑 Audit Logging

<p align="center">
    <img src="docs/ETL audit.png" width="100%">
</p>

Every ETL execution is logged into:

```text
warehouse.etl_audit
```

Information captured:

- Pipeline Name
- Status
- Rows Processed
- Rows Failed
- Duration
- Execution Time

---

# 🐳 Docker Services

<p align="center">
    <img src="docs/docker containers.png" width="100%">
</p>

The platform runs entirely inside Docker.

Containers:

- PostgreSQL
- Apache Kafka
- Zookeeper
- Apache Spark Master
- Apache Spark Worker
- Apache Airflow Scheduler
- Apache Airflow Webserver

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/your-username/retail-data-engineering-platform.git

cd retail-data-engineering-platform
```

---

## Start Docker

```bash
docker compose up -d
```

---

## Start Spark Streaming

```bash
python -m streaming.spark_streaming
```

---

## Produce Streaming Events

```bash
python -m streaming.producer
```

---

## Run Warehouse ETL

```bash
python -m warehouse.loaders.load_warehouse
```

---

## Open Airflow

```
http://localhost:8080
```

---

# 📈 Example Warehouse Tables

```
warehouse.dim_customer

warehouse.dim_product

warehouse.dim_date

warehouse.fact_sales

warehouse.etl_audit
```

---

# 🔍 Future Improvements

- AWS S3 Integration
- Snowflake Warehouse
- dbt Transformations
- GitHub Actions CI/CD
- Power BI Dashboard
- Data Lineage
- Monitoring Dashboard
- Slack Notifications

---

# 🎯 Learning Outcomes

This project demonstrates experience with:

- Event Streaming
- ETL Development
- Spark Structured Streaming
- Apache Airflow
- Data Warehousing
- Star Schema Modeling
- PostgreSQL
- Docker
- Data Quality
- Audit Logging
- Production Logging

---

# 👨‍💻 Author

**Jay Patel**

Computer Science Student

Aspiring Data Engineer  

---

# 📜 License

This project is licensed under the MIT License.