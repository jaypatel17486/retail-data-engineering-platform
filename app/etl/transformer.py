from utils.logger import app_logger


class Transformer:

    @staticmethod
    def transform(df):

        app_logger.info("Removing duplicates")

        df = df.drop_duplicates()

        app_logger.info("Replacing null values")

        df = df.fillna("Unknown")

        return df