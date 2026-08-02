import time

from warehouse.loaders.load_dimensions import main as load_dimensions
from warehouse.loaders.load_fact_sales import main as load_fact_sales

from utils.logger import warehouse_logger
from quality.audit import write_audit_log


def main():

    start = time.time()

    warehouse_logger.info("=" * 60)
    warehouse_logger.info("Warehouse Refresh Started")

    try:

        load_dimensions()

        load_fact_sales()

        duration = time.time() - start

        warehouse_logger.info("Calling write_audit_log()")

        write_audit_log(
            pipeline_name="retail_etl",
            status="SUCCESS",
            rows_processed=0,
            rows_failed=0,
            duration_seconds=duration,
            message="Warehouse refresh completed successfully",
        )

        warehouse_logger.info("write_audit_log() finished")

    except Exception as e:

        duration = time.time() - start

        warehouse_logger.exception("Warehouse Refresh Failed")

        write_audit_log(
            pipeline_name="retail_etl",
            status="FAILED",
            rows_processed=0,
            rows_failed=1,
            duration_seconds=duration,
            message=str(e),
        )

        raise


if __name__ == "__main__":
    main()