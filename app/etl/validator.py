from app.utils.logger import logger


class Validator:

    @staticmethod
    def validate(df):

        logger.info("Validating dataset")

        if df.empty:
            raise ValueError("Dataset is empty.")

        return df