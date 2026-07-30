class DuplicateCheck:

    @staticmethod
    def run(df):

        duplicates = df.duplicated().sum()

        if duplicates > 0:

            print(f"Removed {duplicates} duplicate rows")

            df = df.drop_duplicates()

        return df