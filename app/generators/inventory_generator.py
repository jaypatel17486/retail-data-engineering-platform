from pathlib import Path
import random

import pandas as pd

OUTPUT_DIR = Path("data/raw")

products = pd.read_csv(OUTPUT_DIR / "products.csv")
stores = pd.read_csv(OUTPUT_DIR / "stores.csv")


def generate_inventory():

    inventory = []

    inventory_id = 1

    for _, store in stores.iterrows():

        for _, product in products.iterrows():

            inventory.append(
                {
                    "inventory_id": inventory_id,
                    "product_id": int(product["product_id"]),
                    "store_id": int(store["store_id"]),
                    "quantity": random.randint(10, 500),
                }
            )

            inventory_id += 1

    df = pd.DataFrame(inventory)

    output_file = OUTPUT_DIR / "inventory.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} inventory records")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    generate_inventory()