-- =====================================================
-- FACT TABLE INDEXES
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_fact_sales_customer
ON warehouse.fact_sales(customer_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_product
ON warehouse.fact_sales(product_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_date
ON warehouse.fact_sales(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_order
ON warehouse.fact_sales(order_id);

-- =====================================================
-- DIMENSION INDEXES
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_dim_customer_customer_id
ON warehouse.dim_customer(customer_id);

CREATE INDEX IF NOT EXISTS idx_dim_product_product_id
ON warehouse.dim_product(product_id);

CREATE INDEX IF NOT EXISTS idx_dim_date_full_date
ON warehouse.dim_date(full_date);