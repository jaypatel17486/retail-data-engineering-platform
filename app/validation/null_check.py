class NullCheck:

    @staticmethod
    def run(df):

        if df.isnull().sum().sum() > 0:

            print("Null values detected")

            df = df.fillna("Unknown")

        return df