from warehouse.loaders.database import get_connection
from utils.logger import warehouse_logger

class DimensionLoader:

    def __init__(self):
        self.conn = get_connection()
        self.cur = self.conn.cursor()

    def load_customers(self):
        warehouse_logger.info("Loading Customer Dimension...")

        self.cur.execute("""
            INSERT INTO warehouse.dim_customer
            (
                customer_id
            )
            SELECT DISTINCT
                customer_id
            FROM streaming_orders
            WHERE customer_id IS NOT NULL
            ON CONFLICT (customer_id)
            DO NOTHING;
        """)

        warehouse_logger.info(
            "Customer Dimension Loaded (%s rows)",
            self.cur.rowcount,
        )

    def load_products(self):
        warehouse_logger.info("Loading Product Dimension...")

        self.cur.execute("""
            INSERT INTO warehouse.dim_product
            (
                product_id
            )
            SELECT DISTINCT
                product_id
            FROM streaming_orders
            WHERE product_id IS NOT NULL
            ON CONFLICT (product_id)
            DO NOTHING;
        """)

        warehouse_logger.info(
            "Product Dimension Loaded (%s rows)",
            self.cur.rowcount,
        )

    def load_dates(self):
        warehouse_logger.info("Loading Date Dimension...")

        self.cur.execute("""
            INSERT INTO warehouse.dim_date
            (
                date_key,
                full_date,
                year,
                quarter,
                month,
                month_name,
                day,
                weekday
            )

            SELECT DISTINCT

                TO_CHAR(
                    timestamp::timestamp,
                    'YYYYMMDD'
                )::INTEGER,

                DATE(timestamp::timestamp),

                EXTRACT(
                    YEAR FROM timestamp::timestamp
                )::INTEGER,

                EXTRACT(
                    QUARTER FROM timestamp::timestamp
                )::INTEGER,

                EXTRACT(
                    MONTH FROM timestamp::timestamp
                )::INTEGER,

                TRIM(
                    TO_CHAR(
                        timestamp::timestamp,
                        'Month'
                    )
                ),

                EXTRACT(
                    DAY FROM timestamp::timestamp
                )::INTEGER,

                TRIM(
                    TO_CHAR(
                        timestamp::timestamp,
                        'Day'
                    )
                )

            FROM streaming_orders

            WHERE timestamp IS NOT NULL

            ON CONFLICT (date_key)
            DO NOTHING;
        """)

        warehouse_logger.info(
            "Date Dimension Loaded (%s rows)",
            self.cur.rowcount,
        )

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()


def main():

    warehouse_logger.info("=" * 60)
    warehouse_logger.info("Dimension Load Started")
    warehouse_logger.info("=" * 60)

    loader = DimensionLoader()

    try:

        loader.load_customers()

        loader.load_products()

        loader.load_dates()

        loader.commit()

        warehouse_logger.info(
            "Dimension Load Completed Successfully"
        )

    except Exception:

        loader.rollback()

        warehouse_logger.exception(
            "Dimension Load Failed"
        )

        raise

    finally:

        loader.close()


if __name__ == "__main__":
    main()