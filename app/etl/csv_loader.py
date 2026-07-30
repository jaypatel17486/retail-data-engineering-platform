import pandas as pd


class CSVLoader:

    @staticmethod
    def load(filename: str):
        return pd.read_csv(f"data/raw/{filename}")