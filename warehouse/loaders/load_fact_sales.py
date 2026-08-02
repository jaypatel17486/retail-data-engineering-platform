from warehouse.loaders.database import get_connection
from utils.logger import warehouse_logger

class FactLoader:

    def __init__(self):
        self.conn = get_connection()
        self.cur = self.conn.cursor()

    def load_fact_sales(self):

        warehouse_logger.info("Loading Fact Sales...")

        self.cur.execute("""
            INSERT INTO warehouse.fact_sales
            (
                order_id,
                customer_key,
                product_key,
                date_key,
                quantity,
                price,
                revenue,
                payment_method,
                status
            )

            SELECT
                s.order_id,
                dc.customer_key,
                dp.product_key,
                CAST(TO_CHAR(s.timestamp::timestamp, 'YYYYMMDD') AS INTEGER),
                s.quantity,
                s.price,
                s.quantity * s.price,
                s.payment_method,
                s.status

            FROM streaming_orders s

            JOIN warehouse.dim_customer dc
                ON s.customer_id = dc.customer_id

            JOIN warehouse.dim_product dp
                ON s.product_id = dp.product_id

            ON CONFLICT (order_id)
            DO NOTHING;
        """)

        self.conn.commit()

        print("Fact Sales Loaded Successfully.")

    def close(self):
        self.cur.close()
        self.conn.close()


def main():

    loader = FactLoader()

    loader.load_fact_sales()

    loader.close()


if __name__ == "__main__":
    main()