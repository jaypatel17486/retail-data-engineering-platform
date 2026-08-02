from utils.logger import app_logger


class Validator:

    @staticmethod
    def validate(df):

        app_logger.info("Validating dataset")

        if df.empty:
            raise ValueError("Dataset is empty.")

        return df