class GenericMapper:

    @staticmethod
    def map(df, model):

        objects = []

        for _, row in df.iterrows():

            objects.append(
                model(
                    **row.to_dict()
                )
            )

        return objects