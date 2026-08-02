from config.settings import RAW_DATA_DIR
import pandas as pd

class Extractor:

    @staticmethod
    def read(filename):

        filepath = RAW_DATA_DIR / filename

        return pd.read_csv(filepath)