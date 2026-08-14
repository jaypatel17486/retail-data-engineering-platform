-- =========================================================
-- FLUXGUARD DATABASE
-- =========================================================


-- ---------------------------------------------------------
-- TRANSACTIONS
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS transactions (
    id BIGSERIAL PRIMARY KEY,

    event_id VARCHAR(100) UNIQUE NOT NULL,
    order_id VARCHAR(100) NOT NULL,
    customer_id VARCHAR(100) NOT NULL,

    event_type VARCHAR(50) NOT NULL,

    amount NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',

    payment_method VARCHAR(50),

    device_id VARCHAR(100),
    ip_address VARCHAR(50),

    billing_country VARCHAR(10),
    shipping_country VARCHAR(10),

    failure_reason VARCHAR(100),

    event_timestamp TIMESTAMPTZ NOT NULL,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- ---------------------------------------------------------
-- FRAUD PREDICTIONS
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS fraud_predictions (
    id BIGSERIAL PRIMARY KEY,

    event_id VARCHAR(100) NOT NULL,
    order_id VARCHAR(100) NOT NULL,
    customer_id VARCHAR(100) NOT NULL,

    rule_score INTEGER NOT NULL,
    rule_risk VARCHAR(20) NOT NULL,

    ml_probability NUMERIC(6, 5),
    ml_risk VARCHAR(20),

    hybrid_score NUMERIC(6, 5),

    final_risk VARCHAR(20),
    final_decision VARCHAR(20),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_prediction_transaction
        FOREIGN KEY (event_id)
        REFERENCES transactions(event_id)
        ON DELETE CASCADE
);


-- ---------------------------------------------------------
-- FRAUD ALERTS
-- ---------------------------------------------------------

CREATE TABLE IF NOT EXISTS fraud_alerts (
    id BIGSERIAL PRIMARY KEY,

    event_id VARCHAR(100) NOT NULL,
    order_id VARCHAR(100) NOT NULL,
    customer_id VARCHAR(100) NOT NULL,

    risk_level VARCHAR(20) NOT NULL,

    fraud_score NUMERIC(6, 5),

    decision VARCHAR(20) NOT NULL,

    status VARCHAR(20) DEFAULT 'OPEN',

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    reviewed_at TIMESTAMPTZ,

    CONSTRAINT fk_alert_transaction
        FOREIGN KEY (event_id)
        REFERENCES transactions(event_id)
        ON DELETE CASCADE
);


-- ---------------------------------------------------------
-- INDEXES
-- ---------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_transactions_order
ON transactions(order_id);


CREATE INDEX IF NOT EXISTS idx_transactions_customer
ON transactions(customer_id);


CREATE INDEX IF NOT EXISTS idx_transactions_timestamp
ON transactions(event_timestamp);


CREATE INDEX IF NOT EXISTS idx_predictions_risk
ON fraud_predictions(final_risk);


CREATE INDEX IF NOT EXISTS idx_alerts_status
ON fraud_alerts(status);