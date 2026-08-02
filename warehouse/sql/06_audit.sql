CREATE TABLE IF NOT EXISTS warehouse.etl_audit (

    audit_id SERIAL PRIMARY KEY,

    pipeline_name VARCHAR(100),

    run_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    status VARCHAR(20),

    rows_processed INTEGER,

    rows_failed INTEGER,

    duration_seconds DOUBLE PRECISION,

    message TEXT
);