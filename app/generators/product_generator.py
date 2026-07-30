from pathlib import Path
import random

import pandas as pd

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PRODUCTS = {
    "Electronics": [
        "MacBook Pro",
        "iPhone",
        "Galaxy S",
        "iPad",
        "AirPods",
        "Monitor",
        "Mechanical Keyboard",
        "Gaming Mouse",
    ],
    "Home": [
        "Vacuum Cleaner",
        "Dining Table",
        "Office Chair",
        "Coffee Maker",
        "Blender",
    ],
    "Sports": [
        "Football",
        "Basketball",
        "Yoga Mat",
        "Tennis Racket",
    ],
    "Books": [
        "Python Programming",
        "SQL Handbook",
        "Data Engineering",
        "Machine Learning",
    ],
    "Clothing": [
        "T-Shirt",
        "Jeans",
        "Sneakers",
        "Jacket",
    ],
    "Health": [
        "Protein Powder",
        "Vitamin C",
        "Yoga Ball",
    ],
    "Beauty": [
        "Face Wash",
        "Moisturizer",
        "Shampoo",
    ],
    "Toys": [
        "Lego Set",
        "RC Car",
        "Puzzle",
    ],
    "Furniture": [
        "Bookshelf",
        "Desk",
        "Sofa",
    ],
    "Groceries": [
        "Rice",
        "Pasta",
        "Olive Oil",
    ],
}


def generate_products():

    products = []

    product_id = 1

    category_id = 1

    for category_name, items in PRODUCTS.items():

        for item in items:

            sku = (
                category_name[:3].upper()
                + "-"
                + str(product_id).zfill(4)
            )

            products.append(
                {
                    "product_id": product_id,
                    "sku": sku,
                    "product_name": item,
                    "category_id": category_id,
                    "supplier_id": random.randint(1, 200),
                    "price": round(random.uniform(10, 2500), 2),
                    "stock_quantity": random.randint(20, 500),
                }
            )

            product_id += 1

        category_id += 1

    df = pd.DataFrame(products)

    output_file = OUTPUT_DIR / "products.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} products")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    generate_products()