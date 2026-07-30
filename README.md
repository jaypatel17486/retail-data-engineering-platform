Retail Data Engineering Platform

End-to-end data engineering platform built with
Python • PostgreSQL • Airflow • Kafka • Spark • Docker

---------------------------------------------------

Architecture Diagram
                Retail Data Engineering Platform

                  Batch Pipeline
      ┌─────────────────────────────────────┐
      │                                     │
CSV Generator ─► ETL ─► Airflow ─► PostgreSQL
      │                                     │
      └─────────────────────────────────────┘


               Streaming Pipeline
      ┌─────────────────────────────────────┐
      │                                     │
Order Generator ─► Kafka ─► Consumer ─► PostgreSQL
      │                                     │
      └─────────────────────────────────────┘


               Future Analytics
                     │
                     ▼
                  Spark
                     │
                     ▼
                 Snowflake
                     │
                     ▼
                  Power BI
Project Overview

Tech Stack

Features

Project Structure

Installation

Pipeline Walkthrough

Screenshots

Future Improvements

Author