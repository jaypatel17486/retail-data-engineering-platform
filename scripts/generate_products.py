import random
from pathlib import Path

import pandas as pd

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

categories = {
    "Electronics": [
        "Laptop",
        "Smartphone",
        "Monitor",
        "Keyboard",
        "Mouse",
        "Tablet",
        "Smartwatch"
    ],
    "Home": [
        "Chair",
        "Table",
        "Lamp",
        "Sofa",
        "Curtains"
    ],
    "Sports": [
        "Football",
        "Basketball",
        "Tennis Racket",
        "Yoga Mat"
    ],
    "Books": [
        "Python Programming",
        "SQL Guide",
        "Data Engineering",
        "Machine Learning"
    ],
    "Clothing": [
        "T-Shirt",
        "Jeans",
        "Jacket",
        "Shoes"
    ]
}

products = []
product_id = 1

for category, items in categories.items():
    for item in items:
        products.append({
            "product_id": product_id,
            "product_name": item,
            "category": category,
            "price": round(random.uniform(10, 2000), 2),
            "stock_quantity": random.randint(20, 500)
        })
        product_id += 1

df = pd.DataFrame(products)

output_file = OUTPUT_DIR / "products.csv"
df.to_csv(output_file, index=False)

print(f"Generated {len(df)} products")
print(f"Saved to {output_file}")