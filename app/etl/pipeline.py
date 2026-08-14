from app.etl.extractor import Extractor
from app.etl.validator import Validator
from app.etl.transformer import Transformer
from app.etl.generic_mapper import GenericMapper
from app.etl.database_loader import DatabaseLoader
from app.models.customer import Customer
from utils.logger import app_logger
from app.validation.quality import DataQuality

import time


class Pipeline:

    @staticmethod
    def run(filename: str, model):

        # Start timer
        start_time = time.time()

        app_logger.info("=" * 60)
        app_logger.info(f"Starting ETL Pipeline for {filename}")
        app_logger.info("=" * 60)

        try:

            # Extract
            df = Extractor.read(filename)

            # Validate
            df = Validator.validate(df)

            # Data Quality Checks
            df = DataQuality.run(df)

            # Transform
            df = Transformer.transform(df)

            app_logger.info(f"Processing {len(df)} records")

            # Map DataFrame to SQLAlchemy objects
            objects = GenericMapper.map(
                df,
                model
            )

            # Load into PostgreSQL
            loader = DatabaseLoader()

            loader.load(
                table_name=model.__tablename__,
                objects=objects,
            )

            loader.close()

            # End timer
            end_time = time.time()

            latency_seconds = end_time - start_time
            latency_minutes = latency_seconds / 60

            app_logger.info(
                f"{filename} loaded successfully!"
            )

            app_logger.info(
                f"Records processed: {len(df)}"
            )

            app_logger.info(
                f"Pipeline execution time: "
                f"{latency_seconds:.2f} seconds "
                f"({latency_minutes:.2f} minutes)"
            )

            app_logger.info("=" * 60)

        except Exception as e:

            end_time = time.time()

            latency_seconds = end_time - start_time

            app_logger.error(
                f"Pipeline failed after "
                f"{latency_seconds:.2f} seconds"
            )

            app_logger.error(str(e))

            raise


def main():

    Pipeline.run(
        filename="customers.csv",
        model=Customer,
    )


if __name__ == "__main__":
    main()