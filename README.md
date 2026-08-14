# FluxGuard

### Real-Time E-Commerce Analytics & Fraud Detection Platform

FluxGuard is an end-to-end real-time data engineering and fraud detection platform that processes simulated e-commerce transactions, detects suspicious activity using rule-based logic and a PyTorch machine learning model, stores operational and analytical data in PostgreSQL, and exposes live analytics through FastAPI and a React dashboard.

The project combines **Data Engineering, Backend Engineering, Machine Learning, and Real-Time Analytics** in a single system.

---

## Key Features

- Real-time e-commerce transaction generation
- Apache Kafka event streaming
- Apache Spark Structured Streaming
- Correlated order and payment events
- Rule-based fraud detection
- PyTorch fraud classification model
- Hybrid fraud scoring
- PostgreSQL operational database
- Dimensional analytics warehouse
- Apache Airflow orchestration
- Automated data-quality checks
- FastAPI REST API
- React real-time dashboard
- Fraud alerts and risk monitoring
- Idempotent warehouse loading

---

# Architecture

```text
                         FLUXGUARD

                 E-Commerce Transaction
                           |
                           v
                  Transaction Producer
                           |
                           v
                     Apache Kafka
                  (fluxguard-events)
                           |
             +-------------+-------------+
             |                           |
             v                           v
     Spark Structured              Fraud Consumer
        Streaming                        |
             |                           v
             |                   Feature Engineering
             |                           |
             |                +----------+----------+
             |                |                     |
             |                v                     v
             |          Rule Engine          PyTorch Model
             |                |                     |
             |                +----------+----------+
             |                           |
             |                           v
             |                    Hybrid Decision
             |                           |
             +---------------------------+
                                         |
                                         v
                                    PostgreSQL
                                         |
                         +---------------+---------------+
                         |                               |
                         v                               v
                      FastAPI                         Airflow
                         |                               |
                         v                               v
                  React Dashboard                 Data Quality
                                                         |
                                                         v
                                                 Analytics Warehouse
                                                         |
                                                         v
                                               Historical Analytics
```

---

# Real-Time Event Pipeline

FluxGuard generates correlated e-commerce transaction events.

Example lifecycle:

```text
order_created
      |
      | same order_id
      | same customer_id
      | same amount
      v
payment_completed
```

or:

```text
order_created
      |
      v
payment_failed
```

Example event:

```json
{
  "event_id": "evt_a6e656f94982",
  "event_type": "payment_completed",
  "order_id": "ORD-245842",
  "customer_id": "CUS-0536",
  "amount": 322.75,
  "currency": "USD",
  "payment_method": "debit_card",
  "device_id": "DEV-2811",
  "billing_country": "US",
  "shipping_country": "US"
}
```

Events are published to:

```text
fluxguard-events
```

The `order_id` is used as the Kafka message key so events belonging to the same order can be partitioned consistently.

---

# Fraud Detection

FluxGuard uses a hybrid fraud-detection architecture.

## Rule Engine

The rule engine evaluates signals such as:

- High transaction amount
- Very high transaction amount
- Billing/shipping country mismatch
- Failed payment
- Suspected fraud failure reason

It generates:

```text
fraud_score
risk_level
fraud_reasons
is_suspicious
```

Risk levels:

```text
0 - 29     LOW
30 - 59    MEDIUM
60 - 100   HIGH
```

---

## PyTorch Model

FluxGuard also includes a neural-network fraud classifier built with PyTorch.

Current model features include:

```text
amount
country_mismatch
payment_failed
suspected_fraud_failure
```

Architecture:

```text
4 input features
       |
       v
Linear(4, 16)
       |
      ReLU
       |
       v
Linear(16, 8)
       |
      ReLU
       |
       v
Linear(8, 1)
       |
       v
Fraud Probability
```

The training pipeline performs:

- Synthetic labeled dataset generation
- Train/validation/test splitting
- Feature standardization
- Class-imbalance weighting
- PyTorch training
- Model evaluation
- Model persistence
- Real-time inference

Evaluation includes:

```text
Accuracy
Precision
Recall
F1 Score
ROC-AUC
```

> The current model is trained on synthetic transaction data and is intended to demonstrate the complete ML engineering pipeline rather than production financial fraud detection.

---

# Hybrid Fraud Engine

FluxGuard combines explainable rules with ML predictions.

```text
                    Payment
                       |
            +----------+----------+
            |                     |
            v                     v
       Rule Engine           PyTorch Model
            |                     |
       Rule Score            Probability
            |                     |
            +----------+----------+
                       |
                       v
                  Hybrid Score
                       |
              +--------+--------+
              |        |        |
              v        v        v
           APPROVE   REVIEW   BLOCK
```

The current experimental hybrid calculation is:

```text
40% Rule Score
+
60% ML Probability
```

This weighting is configurable and is not presented as an industry-standard fraud policy.

---

# Apache Spark

Spark Structured Streaming consumes FluxGuard events from Kafka.

Responsibilities include:

- Kafka ingestion
- JSON parsing
- Schema enforcement
- Event validation
- Timestamp conversion
- Event deduplication
- Watermarking
- Order/payment stream separation
- Fraud feature preparation

Example flow:

```text
Kafka
  |
  v
Spark Structured Streaming
  |
  v
Parse JSON
  |
  v
Validate
  |
  v
Deduplicate event_id
  |
  +-------------------+
  |                   |
  v                   v
Orders              Payments
```

---

# PostgreSQL

FluxGuard maintains operational tables for the real-time application.

```text
transactions
fraud_predictions
fraud_alerts
```

### Transactions

Stores payment transaction details.

### Fraud Predictions

Stores:

```text
rule_score
rule_risk
ml_probability
ml_risk
hybrid_score
final_risk
final_decision
```

### Fraud Alerts

Stores transactions requiring investigation or blocking.

---

# Analytics Warehouse

FluxGuard includes a separate analytical warehouse schema:

```text
fluxguard_dw
```

Dimensions:

```text
dim_customer
dim_payment_method
dim_date
```

Facts:

```text
fact_transactions
fact_fraud_predictions
fact_fraud_alerts
```

The warehouse loader is designed to be idempotent, allowing pipelines to be rerun without duplicating previously processed events.

---

# Apache Airflow

Airflow orchestrates FluxGuard's batch and historical analytics workflows.

Current pipelines include:

```text
fluxguard_analytics_pipeline
fluxguard_quality_pipeline
```

Example analytics workflow:

```text
Database Check
      |
      v
Data Quality
      |
      v
Warehouse Load
      |
      v
Historical Analytics
```

---

# Data Quality

FluxGuard performs automated checks including:

- Missing event IDs
- Missing order/customer IDs
- Invalid transaction amounts
- Duplicate events
- Orphan fraud predictions
- Invalid ML probabilities
- Invalid hybrid fraud scores

Failed checks can stop downstream warehouse processing.

---

# FastAPI Backend

FluxGuard exposes its operational and analytical data through FastAPI.

Run:

```bash
uvicorn fluxguard_api.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Example endpoints:

```text
GET /health

GET /api/v1/info

GET /api/v1/transactions
GET /api/v1/transactions/{order_id}

GET /api/v1/fraud/alerts
GET /api/v1/fraud/stats

GET /api/v1/analytics/overview
GET /api/v1/analytics/revenue
GET /api/v1/analytics/payments
GET /api/v1/analytics/risk-distribution
GET /api/v1/analytics/recent-activity
```

---

# React Dashboard

FluxGuard includes a React + Vite dashboard.

The dashboard displays:

- Total revenue
- Transaction volume
- Fraud alerts
- Blocked transactions
- Revenue trends
- Payment success rate
- Risk distribution
- ML fraud probability
- Live transaction activity
- Fraud alert activity

During local development, the dashboard periodically refreshes data from the FastAPI backend.

Run:

```bash
cd dashboard
npm install
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

# Technology Stack

| Area | Technology |
|---|---|
| Programming | Python |
| Streaming | Apache Kafka |
| Stream Processing | Apache Spark Structured Streaming |
| Machine Learning | PyTorch |
| Database | PostgreSQL |
| Orchestration | Apache Airflow |
| Backend API | FastAPI |
| Frontend | React |
| Frontend Build Tool | Vite |
| Visualization | Recharts |
| Containers | Docker / Docker Compose |
| Testing | Pytest |
| ML Utilities | scikit-learn, pandas |

---

# Project Structure

```text
fluxguard/
|
├── airflow/
│   └── dags/
│       ├── fluxguard_analytics_pipeline.py
│       └── fluxguard_quality_pipeline.py
|
├── database/
│   └── fluxguard_schema.sql
|
├── dashboard/
│   └── src/
|
├── fluxguard_api/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── routes/
│       ├── analytics.py
│       ├── fraud.py
│       └── transactions.py
|
├── fraud/
│   ├── consumer.py
│   ├── engine.py
│   ├── rules.py
│   ├── evaluation/
│   └── ml/
│       ├── generate_dataset.py
│       ├── model.py
│       ├── predict.py
│       ├── train.py
│       └── models/
|
├── spark/
│   ├── config/
│   ├── jobs/
│   │   ├── streaming.py
│   │   └── fraud_streaming.py
│   └── schemas/
|
├── streaming/
│   ├── events.py
│   └── producer.py
|
├── tests/
│   └── api/
|
├── warehouse/
│   ├── loaders/
│   │   └── load_fluxguard_warehouse.py
│   └── sql/
│       └── fluxguard_warehouse.sql
|
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

# Running FluxGuard Locally

## 1. Clone

```bash
git clone <repository-url>
cd fluxguard
```

## 2. Python environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 3. Environment configuration

```bash
cp .env.example .env
```

Review the values in `.env`.

## 4. Start infrastructure

```bash
docker compose up -d
```

## 5. Initialize operational database

```bash
docker compose exec -T postgres \
  psql -U postgres -d fluxguard \
  < database/fluxguard_schema.sql
```

## 6. Initialize warehouse

```bash
docker compose exec -T postgres \
  psql -U postgres -d fluxguard \
  < warehouse/sql/fluxguard_warehouse.sql
```

## 7. Start fraud consumer

```bash
python -m fraud.consumer
```

## 8. Start transaction producer

In another terminal:

```bash
python -m streaming.producer
```

## 9. Start API

```bash
uvicorn fluxguard_api.main:app --reload
```

## 10. Start dashboard

```bash
cd dashboard
npm install
npm run dev
```

---

# Machine Learning

Generate synthetic training data:

```bash
python -m fraud.ml.generate_dataset
```

Train the PyTorch model:

```bash
python -m fraud.ml.train
```

Evaluate the rule engine:

```bash
python -m fraud.evaluation.evaluate_rules
```

---

# Warehouse

Run the warehouse loader manually:

```bash
python -m warehouse.loaders.load_fluxguard_warehouse
```

The same process can be orchestrated through Airflow.

---

# Testing

Run FluxGuard API tests:

```bash
python -m pytest tests/api -v
```

Additional unit and integration coverage can be added for:

```text
Event generation
Fraud rules
ML inference
Kafka producer/consumer
Warehouse loading
API endpoints
Data quality
```

---

# Engineering Concepts Demonstrated

FluxGuard demonstrates:

### Data Engineering

- Event-driven architecture
- Kafka partitioning
- Structured streaming
- Schema enforcement
- Watermarking
- Deduplication
- Incremental ETL
- Idempotent data loading
- Dimensional modeling
- Workflow orchestration
- Automated data-quality checks

### Software Engineering

- Modular Python architecture
- REST API design
- Connection pooling
- Environment-based configuration
- Dockerized services
- API testing
- Frontend/backend separation

### Machine Learning Engineering

- Synthetic dataset generation
- Feature engineering
- Class imbalance handling
- Neural-network training
- Model serialization
- Real-time inference
- Rule-vs-ML evaluation
- Hybrid decision systems

---

# Current Limitations

FluxGuard is a portfolio and engineering simulation project.

Current limitations include:

- Fraud labels are synthetically generated.
- The ML model is not trained on real financial transaction data.
- Fraud thresholds and hybrid weights are experimental.
- The dashboard currently uses periodic API polling rather than server-pushed events.
- Additional production observability, authentication, and security controls would be required for a real financial system.

---

# Future Improvements

Planned improvements include:

- WebSocket dashboard updates
- Kafka dead-letter topics
- Manual Kafka offset management
- Stronger idempotency guarantees
- Prometheus + Grafana monitoring
- Structured application logging
- ML model versioning
- Automated model retraining
- Feature-store architecture
- Drift monitoring
- API authentication
- CI/CD with GitHub Actions
- Cloud deployment

---

# Why FluxGuard?

The goal of FluxGuard is to demonstrate how multiple engineering disciplines work together in a realistic event-driven system.

Instead of building isolated Kafka, Spark, API, or ML demos, FluxGuard connects them into one pipeline:

```text
Generate
   |
Stream
   |
Process
   |
Detect
   |
Store
   |
Orchestrate
   |
Serve
   |
Visualize
```

This makes the project useful for demonstrating **Data Engineering, Software Engineering, and Machine Learning Engineering** skills in one system.

---

## License

See [LICENSE](LICENSE).