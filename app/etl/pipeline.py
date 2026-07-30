from app.etl.extractor import Extractor
from app.etl.validator import Validator
from app.etl.transformer import Transformer
from app.etl.generic_mapper import GenericMapper
from app.etl.database_loader import DatabaseLoader
from app.models.customer import Customer
from app.utils.logger import logger
from app.validation.quality import DataQuality


class Pipeline:

    @staticmethod
    def run(filename: str, model):

        logger.info("=" * 60)
        logger.info(f"Starting ETL Pipeline for {filename}")
        logger.info("=" * 60)

        # Extract
        df = Extractor.read(filename)

        from app.validation.quality import DataQuality

        df = Validator.validate(df)

        df = DataQuality.run(df)

        df = Transformer.transform(df)

        logger.info(f"Processing {len(df)} records")

        # Map DataFrame to SQLAlchemy objects
        objects = GenericMapper.map(df, model)

        # Load into PostgreSQL
        loader = DatabaseLoader()

        loader.load(
            table_name=model.__tablename__,
            objects=objects,
        )

        loader.close()

        logger.info(f"{filename} loaded successfully!")
        logger.info("=" * 60)


def main():

    Pipeline.run(
        filename="customers.csv",
        model=Customer,
    )


if __name__ == "__main__":
    main()