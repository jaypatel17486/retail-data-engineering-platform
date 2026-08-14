CREATE SCHEMA IF NOT EXISTS fluxguard_dw;


-- =========================================================
-- DIMENSION: CUSTOMER
-- =========================================================

CREATE TABLE IF NOT EXISTS fluxguard_dw.dim_customer (
    customer_key BIGSERIAL PRIMARY KEY,
    customer_id VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- =========================================================
-- DIMENSION: PAYMENT METHOD
-- =========================================================

CREATE TABLE IF NOT EXISTS fluxguard_dw.dim_payment_method (
    payment_method_key BIGSERIAL PRIMARY KEY,
    payment_method VARCHAR(50) UNIQUE NOT NULL
);


-- =========================================================
-- DIMENSION: DATE
-- =========================================================

CREATE TABLE IF NOT EXISTS fluxguard_dw.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    day INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL
);


-- =========================================================
-- FACT: TRANSACTIONS
-- =========================================================

CREATE TABLE IF NOT EXISTS fluxguard_dw.fact_transactions (
    transaction_key BIGSERIAL PRIMARY KEY,

    event_id VARCHAR(100) UNIQUE NOT NULL,
    order_id VARCHAR(100) NOT NULL,

    customer_key BIGINT
        REFERENCES fluxguard_dw.dim_customer(customer_key),

    payment_method_key BIGINT
        REFERENCES fluxguard_dw.dim_payment_method(payment_method_key),

    date_key INTEGER
        REFERENCES fluxguard_dw.dim_date(date_key),

    event_type VARCHAR(50) NOT NULL,

    amount NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(10),

    billing_country VARCHAR(10),
    shipping_country VARCHAR(10),

    event_timestamp TIMESTAMPTZ NOT NULL
);


-- =========================================================
-- FACT: FRAUD PREDICTIONS
-- =========================================================

CREATE TABLE IF NOT EXISTS fluxguard_dw.fact_fraud_predictions (
    prediction_key BIGSERIAL PRIMARY KEY,

    event_id VARCHAR(100) UNIQUE NOT NULL,
    order_id VARCHAR(100) NOT NULL,

    rule_score INTEGER,
    ml_probability NUMERIC(6, 5),
    hybrid_score NUMERIC(6, 5),

    final_risk VARCHAR(20),
    final_decision VARCHAR(20),

    created_at TIMESTAMPTZ
);


-- =========================================================
-- FACT: FRAUD ALERTS
-- =========================================================

CREATE TABLE IF NOT EXISTS fluxguard_dw.fact_fraud_alerts (
    alert_key BIGSERIAL PRIMARY KEY,

    event_id VARCHAR(100) NOT NULL,
    order_id VARCHAR(100) NOT NULL,

    risk_level VARCHAR(20),
    fraud_score NUMERIC(6, 5),

    decision VARCHAR(20),
    status VARCHAR(20),

    created_at TIMESTAMPTZ
);


-- =========================================================
-- INDEXES
-- =========================================================

CREATE INDEX IF NOT EXISTS idx_fact_transactions_timestamp
ON fluxguard_dw.fact_transactions(event_timestamp);

CREATE INDEX IF NOT EXISTS idx_fact_transactions_customer
ON fluxguard_dw.fact_transactions(customer_key);

CREATE INDEX IF NOT EXISTS idx_fact_fraud_risk
ON fluxguard_dw.fact_fraud_predictions(final_risk);

CREATE INDEX IF NOT EXISTS idx_fact_fraud_decision
ON fluxguard_dw.fact_fraud_predictions(final_decision);