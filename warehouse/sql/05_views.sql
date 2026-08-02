CREATE OR REPLACE VIEW warehouse.v_sales_summary AS

SELECT

    d.year,

    d.month,

    d.month_name,

    COUNT(*) AS total_orders,

    SUM(f.quantity) AS total_quantity,

    ROUND(SUM(f.revenue)::numeric,2) AS total_revenue,

    ROUND(AVG(f.revenue)::numeric,2) AS average_order_value

FROM warehouse.fact_sales f

JOIN warehouse.dim_date d

ON f.date_key = d.date_key

GROUP BY

d.year,
d.month,
d.month_name

ORDER BY

d.year,
d.month;

CREATE OR REPLACE VIEW warehouse.v_top_products AS

SELECT

    p.product_id,

    COUNT(*) total_orders,

    SUM(f.quantity) quantity_sold,

    ROUND(SUM(f.revenue)::numeric,2) revenue

FROM warehouse.fact_sales f

JOIN warehouse.dim_product p

ON f.product_key = p.product_key

GROUP BY

p.product_id

ORDER BY revenue DESC;

CREATE OR REPLACE VIEW warehouse.v_top_customers AS

SELECT

    c.customer_id,

    COUNT(*) total_orders,

    ROUND(SUM(f.revenue)::numeric,2) total_spent

FROM warehouse.fact_sales f

JOIN warehouse.dim_customer c

ON f.customer_key = c.customer_key

GROUP BY

c.customer_id

ORDER BY total_spent DESC;