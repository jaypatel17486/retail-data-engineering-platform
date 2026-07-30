from app.utils.logger import logger


class Transformer:

    @staticmethod
    def transform(df):

        logger.info("Removing duplicates")

        df = df.drop_duplicates()

        logger.info("Replacing null values")

        df = df.fillna("Unknown")

        return df