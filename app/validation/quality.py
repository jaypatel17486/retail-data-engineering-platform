from app.validation.duplicate_check import DuplicateCheck
from app.validation.null_check import NullCheck
from app.validation.schema_check import SchemaCheck


class DataQuality:

    @staticmethod
    def run(df):

        df = SchemaCheck.run(df)

        df = DuplicateCheck.run(df)

        df = NullCheck.run(df)

        return df