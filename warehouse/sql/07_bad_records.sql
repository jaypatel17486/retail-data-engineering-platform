CREATE TABLE IF NOT EXISTS warehouse.bad_records (

    id SERIAL PRIMARY KEY,

    order_id INTEGER,

    customer_id INTEGER,

    product_id INTEGER,

    reason TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);