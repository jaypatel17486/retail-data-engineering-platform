class SchemaCheck:

    @staticmethod
    def run(df):

        if df.empty:
            raise ValueError("Dataset is empty.")

        return df