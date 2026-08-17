# 🛒 Retail Data Engineering Platform

### End-to-End Streaming, ETL & Data Warehousing Platform

An end-to-end **Data Engineering platform** designed to ingest retail transaction events, process streaming data, validate and transform records, and load analytics-ready data into a dimensional warehouse.

The project demonstrates a complete modern data pipeline using **Python, Apache Kafka, Apache Spark, Apache Airflow, PostgreSQL, Docker, and dimensional data modeling**.

---

## 🚀 Project Overview

The Retail Data Engineering Platform was built to demonstrate how raw retail transaction events can move through a production-style data engineering workflow.

The platform covers the complete lifecycle of data:

```text
Generate
   ↓
Ingest
   ↓
Validate
   ↓
Transform
   ↓
Load
   ↓
Model
   ↓
Analyze
```

The project combines:

* Event-driven data ingestion
* Stream processing
* ETL pipeline development
* Data-quality validation
* Workflow orchestration
* Relational data modeling
* Dimensional modeling
* Data warehousing
* Audit logging
* Containerized infrastructure

---

# 🏗️ Architecture

```text
                  RETAIL DATA PLATFORM

                 Retail Data Generator
                         │
                         ▼
                   Apache Kafka
                         │
                         ▼
                     Apache Spark
                         │
                 Stream Processing
                         │
                         ▼
                     PostgreSQL
                         │
                  ETL / Modeling
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       Data Validation        Apache Airflow
                                    │
                                    ▼
                              retail_etl
                                    │
                                    ▼
                           Load Dimensions
                                    │
                                    ▼
                            Load Fact Sales
                                    │
                                    ▼
                             Audit Logging
                                    │
                                    ▼
                         Analytics Warehouse
```

---

# ⚡ Key Engineering Highlights

* Processed **1,111+ retail transaction events**
* Built a **5-stage ETL pipeline**
* Implemented **14 PostgreSQL data models**
* Designed an analytics-ready **Star Schema**
* Used **Apache Kafka** for event streaming
* Used **Apache Spark Structured Streaming** for stream processing
* Used **Apache Airflow** for pipeline orchestration
* Added data-quality validation throughout the ETL workflow
* Implemented dimensional and fact-table loading
* Added ETL audit logging
* Containerized the environment using **Docker**
* Achieved a measured **0.39-second ETL execution time**

---

# 🔄 ETL Pipeline

The core pipeline follows five stages:

```text
┌─────────────┐
│   EXTRACT   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  VALIDATE   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│DATA QUALITY │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  TRANSFORM  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    LOAD     │
└─────────────┘
```

## 1. Extract

Retail transaction data enters the platform and is prepared for downstream processing.

The architecture uses **Apache Kafka** as the event-streaming layer.

---

## 2. Validate

Incoming records are validated before being accepted into downstream analytical workflows.

Validation helps prevent malformed or incomplete records from contaminating transformed datasets.

---

## 3. Data Quality

Data-quality checks are applied before warehouse loading.

This stage helps ensure that downstream analytical tables contain consistent and usable data.

---

## 4. Transform

Raw retail events are converted into structured, analytics-ready records.

Transformations prepare the data for relational and dimensional models.

---

## 5. Load

Validated and transformed records are loaded into the analytical data model.

The Airflow workflow follows the dependency:

```text
Load Dimensions
       │
       ▼
Load Fact Sales
       │
       ▼
Audit Logging
```

Loading dimensions before the fact table preserves the intended dimensional-model relationships.

---

# 📡 Streaming Pipeline

The project demonstrates an event-driven architecture built around Kafka and Spark.

```text
Retail Events
     │
     ▼
Apache Kafka
     │
     ▼
Apache Spark
     │
     ▼
Process / Transform
     │
     ▼
PostgreSQL
```

### Apache Kafka

Kafka provides the streaming ingestion layer for retail transaction events.

It decouples event production from downstream processing and provides the foundation for the streaming architecture.

### Apache Spark

Spark provides the processing layer between Kafka and downstream storage.

The platform uses Spark Structured Streaming as part of the retail transaction processing workflow.

---

# 🗄️ Data Warehouse

The project transforms operational retail data into an analytics-oriented dimensional model.

The documented Star Schema centers around:

```text
                    dim_customer
                         │
                         │
                         ▼
dim_product ───────► fact_sales ◄─────── dim_date
```

The dimensional model separates descriptive business attributes from measurable sales activity.

---

## Dimension Tables

### `dim_customer`

Contains customer-related attributes used for analytical grouping and filtering.

### `dim_product`

Contains product-related descriptive attributes.

### `dim_date`

Provides a reusable date dimension for time-based analysis.

---

## Fact Table

### `fact_sales`

Acts as the central fact table for retail sales analytics.

```text
              dim_customer
                    │
                    ▼
dim_product → fact_sales ← dim_date
```

This design supports analytical questions across dimensions such as:

* Customer
* Product
* Date
* Sales activity

---

# 🧱 Data Modeling

The project includes **14 PostgreSQL data models** across the platform.

The modeling layer demonstrates concepts including:

* Relational modeling
* Dimensional modeling
* Fact and dimension separation
* Analytical warehouse design
* ETL dependency management

The warehouse is structured to transform raw operational data into datasets better suited for analytical workloads.

---

# 🌬️ Apache Airflow

**Apache Airflow** orchestrates the ETL workflow.

The documented DAG is:

```text
retail_etl
```

Its high-level dependency flow is:

```text
retail_etl
    │
    ▼
Load Dimensions
    │
    ▼
Load Fact Sales
    │
    ▼
Audit Logging
```

Airflow provides explicit dependencies between warehouse-loading stages and makes the ETL process repeatable and observable.

---

# 🔍 Data Quality

Data quality is incorporated as a dedicated stage of the pipeline rather than being treated only as a final check.

```text
Extract
   │
   ▼
Validate
   │
   ▼
Data Quality
   │
   ▼
Transform
   │
   ▼
Load
```

This design helps catch problematic records before they propagate into downstream analytical models.

---

# 📋 Audit Logging

The Airflow workflow includes an **audit logging** stage after warehouse loading.

```text
Dimensions
    ↓
Fact Sales
    ↓
Audit Log
```

Audit information provides visibility into ETL execution and helps make pipeline behavior easier to track.

---

# 🛠️ Technology Stack

| Area                             | Technology                        |
| -------------------------------- | --------------------------------- |
| Programming                      | Python                            |
| Query Language                   | SQL                               |
| Event Streaming                  | Apache Kafka                      |
| Stream Processing                | Apache Spark Structured Streaming |
| Workflow Orchestration           | Apache Airflow                    |
| Operational / Warehouse Database | PostgreSQL                        |
| Data Modeling                    | Star Schema                       |
| Infrastructure                   | Docker                            |
| Data Engineering                 | ETL Pipelines                     |
| Warehousing                      | Dimensional Modeling              |

---

# 📊 Project Results

| Metric                  |          Result |
| ----------------------- | --------------: |
| Retail Events Processed |      **1,111+** |
| PostgreSQL Data Models  |          **14** |
| ETL Stages              |           **5** |
| Measured ETL Execution  |    **0.39 sec** |
| Warehouse Model         | **Star Schema** |

These measurements demonstrate the project at its current portfolio-scale workload and should not be interpreted as production-scale performance benchmarks.

---

# 🔁 End-to-End Data Flow

```text
                    RAW RETAIL DATA
                           │
                           ▼
                    EVENT GENERATION
                           │
                           ▼
                      APACHE KAFKA
                           │
                           ▼
                      APACHE SPARK
                           │
                           ▼
                       VALIDATION
                           │
                           ▼
                     DATA QUALITY
                           │
                           ▼
                      TRANSFORM
                           │
                           ▼
                      POSTGRESQL
                           │
                           ▼
                    APACHE AIRFLOW
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
          DIMENSIONS              FACT SALES
                └──────────┬──────────┘
                           ▼
                     AUDIT LOGGING
                           │
                           ▼
                 ANALYTICS WAREHOUSE
```

---

# 🧠 Engineering Concepts Demonstrated

## Data Engineering

* ETL pipeline design
* Event-driven architecture
* Stream processing
* Data validation
* Data-quality engineering
* Pipeline orchestration
* Data warehousing
* Dimensional modeling
* Star Schema design
* Audit logging

## Apache Kafka

* Streaming ingestion
* Event-based pipeline architecture
* Producer/consumer separation

## Apache Spark

* Structured Streaming
* Streaming transformations
* Processing Kafka event data

## Apache Airflow

* DAG-based orchestration
* Task dependencies
* Warehouse loading
* ETL scheduling
* Audit workflow integration

## PostgreSQL

* Relational data modeling
* Analytical data modeling
* Fact and dimension tables
* SQL-based transformations

## Infrastructure

* Dockerized development environment
* Reproducible service configuration
* Multi-component data platform architecture

---

# 📁 Repository Structure

The repository currently contains components and documentation from multiple stages of development.

For a dedicated Retail repository, the recommended public structure is:

```text
retail-data-engineering-platform/
│
├── airflow/
│   └── dags/
│       └── retail_etl.py
│
├── src/
│   ├── generators/
│   ├── streaming/
│   ├── processing/
│   └── validation/
│
├── warehouse/
│   ├── loaders/
│   └── sql/
│
├── tests/
│
├── docs/
│   ├── architecture.png
│   ├── warehouse-star-schema.png
│   ├── airflow-retail-etl.png
│   └── etl-audit.png
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── README.md
└── LICENSE
```

> Update this tree to match the final Retail-only repository before publishing.

---

# 📸 Architecture & Pipeline Screenshots

The project documentation includes screenshots for the warehouse, Airflow workflows, ETL auditing, and Docker environment.

Recommended GitHub layout:

### Star Schema

```markdown
![Retail Warehouse Star Schema](docs/warehouse-star-schema.png)
```

### Airflow ETL Pipeline

```markdown
![Retail ETL Airflow DAG](docs/airflow-retail-etl.png)
```

### ETL Audit

```markdown
![ETL Audit](docs/etl-audit.png)
```

### Docker Infrastructure

```markdown
![Docker Infrastructure](docs/docker-container.png)
```

Rename the existing screenshot files to GitHub-friendly filenames before adding these image links.

---

# ⚙️ Running the Project

The uploaded archive does not contain enough Retail-specific implementation detail to verify the exact startup commands without mixing them with the FluxGuard application.

Before publishing this section, add the actual commands used by the Retail implementation.

A typical sequence should document:

```text
1. Start infrastructure
2. Initialize PostgreSQL
3. Start Kafka
4. Start the retail event producer
5. Start Spark processing
6. Start Airflow
7. Run the retail_etl DAG
8. Verify warehouse tables
```

Do not copy FluxGuard startup commands into this repository unless the Retail implementation actually uses them.

---

# 🎯 Why This Project?

The goal of the Retail Data Engineering Platform is to demonstrate how multiple data-engineering technologies can work together as one complete pipeline.

Instead of building isolated demonstrations of Kafka, Spark, Airflow, or PostgreSQL, the project connects the technologies into an end-to-end workflow:

```text
Generate
   ↓
Stream
   ↓
Process
   ↓
Validate
   ↓
Transform
   ↓
Model
   ↓
Load
   ↓
Orchestrate
   ↓
Analyze
```

The project demonstrates practical experience across the data lifecycle—from incoming events to analytics-ready warehouse models.

---

# 🔮 Future Improvements

Potential improvements include:

* Cloud deployment
* CI/CD pipeline
* Expanded automated testing
* Pipeline observability and alerting
* Larger-scale streaming workloads
* Additional dimensional models
* Incremental warehouse loading
* Data lineage
* Schema evolution handling
* Dead-letter queues
* Infrastructure as Code
* Automated data-quality reporting

---

# 👨‍💻 Author

## Jay Patel

Computer Science student at **California State University, Northridge**

Focused on:

* Data Engineering
* Streaming Systems
* ETL Pipelines
* Data Warehousing
* Cloud Data Infrastructure

🌐 **Portfolio:**
[jay-patel-zeta.vercel.app](https://jay-patel-zeta.vercel.app)

💼 **LinkedIn:**
[Add LinkedIn URL](YOUR_LINKEDIN_URL)

---

## ⭐ Support

If you found this project useful or interesting, consider giving the repository a ⭐.

---

<p align="center">
  <b>From raw retail events to analytics-ready data.</b>
</p>
