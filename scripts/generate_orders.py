import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker()

DATA_DIR = Path("data/raw")

customers = pd.read_csv(DATA_DIR / "customers.csv")
products = pd.read_csv(DATA_DIR / "products.csv")

orders = []
order_items = []

NUM_ORDERS = 5000

for order_id in range(1, NUM_ORDERS + 1):

    customer = customers.sample(1).iloc[0]

    order_date = fake.date_time_between(
        start_date="-1y",
        end_date="now"
    )

    status = random.choice([
        "Delivered",
        "Shipped",
        "Processing",
        "Cancelled"
    ])

    orders.append({
        "order_id": order_id,
        "customer_id": customer["customer_id"],
        "order_date": order_date,
        "status": status
    })

    number_of_products = random.randint(1, 5)

    selected_products = products.sample(number_of_products)

    for _, product in selected_products.iterrows():

        quantity = random.randint(1, 4)

        order_items.append({
            "order_id": order_id,
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": product["price"]
        })

orders_df = pd.DataFrame(orders)
order_items_df = pd.DataFrame(order_items)

orders_df.to_csv(DATA_DIR / "orders.csv", index=False)
order_items_df.to_csv(DATA_DIR / "order_items.csv", index=False)

print(f"Generated {len(orders_df)} orders")
print(f"Generated {len(order_items_df)} order items")