CREATE TABLE warehouse.dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INTEGER UNIQUE,
    customer_name VARCHAR(100),
    email VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(50)
);

CREATE TABLE warehouse.dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id INTEGER UNIQUE,
    product_name VARCHAR(100),
    category VARCHAR(100),
    price DOUBLE PRECISION
);

CREATE TABLE warehouse.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    day INTEGER,
    weekday VARCHAR(20)
);