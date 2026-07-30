from app.etl.pipeline import Pipeline

df = Pipeline.run("customers.csv")

print(df.head())