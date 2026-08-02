CREATE TABLE IF NOT EXISTS warehouse.fact_sales (

    sale_key SERIAL PRIMARY KEY,

    order_id INTEGER UNIQUE,

    customer_key INTEGER
        REFERENCES warehouse.dim_customer(customer_key),

    product_key INTEGER
        REFERENCES warehouse.dim_product(product_key),

    date_key INTEGER
        REFERENCES warehouse.dim_date(date_key),

    quantity INTEGER,

    price DOUBLE PRECISION,

    revenue DOUBLE PRECISION,

    payment_method VARCHAR(50),

    status VARCHAR(50)
);