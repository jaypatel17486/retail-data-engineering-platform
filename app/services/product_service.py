import pandas as pd

from app.database.database import SessionLocal
from app.models.product import Product
from app.repositories.base_repository import BaseRepository


class ProductService:

    def load_products(self):

        db = SessionLocal()

        repo = BaseRepository(db)

        df = pd.read_csv("data/raw/products.csv")

        products = []

        for _, row in df.iterrows():

            products.append(
                Product(
                    product_id=int(row["product_id"]),
                    product_name=row["product_name"],
                    sku=row["sku"],
                    supplier_id=int(row["supplier_id"]),
                    category_id=int(row["category_id"]),
                    price=float(row["price"]),
                    stock_quantity=int(row["stock_quantity"]),
                )
            )

        repo.add_many(products)

        db.close()

        print(f"Inserted {len(products)} products")