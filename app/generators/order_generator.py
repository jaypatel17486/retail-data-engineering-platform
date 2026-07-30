from pathlib import Path
import random

import pandas as pd
from faker import Faker

fake = Faker()

OUTPUT_DIR = Path("data/raw")

customers = pd.read_csv(OUTPUT_DIR / "customers.csv")
products = pd.read_csv(OUTPUT_DIR / "products.csv")


def generate_orders(num_orders=5000):

    orders = []
    order_items = []

    order_item_id = 1

    for order_id in range(1, num_orders + 1):

        customer = customers.sample(1).iloc[0]

        order_date = fake.date_time_between(
            start_date="-1y",
            end_date="now"
        )

        status = random.choice(
            [
                "Delivered",
                "Processing",
                "Cancelled",
                "Shipped",
            ]
        )

        orders.append(
            {
                "order_id": order_id,
                "customer_id": int(customer.customer_id),
                "order_date": order_date,
                "status": status,
            }
        )

        number_of_products = random.randint(1, 5)

        selected_products = products.sample(number_of_products)

        for _, product in selected_products.iterrows():

            quantity = random.randint(1, 3)

            order_items.append(
                {
                    "order_item_id": order_item_id,
                    "order_id": order_id,
                    "product_id": int(product.product_id),
                    "quantity": quantity,
                    "unit_price": float(product.price),
                }
            )

            order_item_id += 1

    orders_df = pd.DataFrame(orders)
    order_items_df = pd.DataFrame(order_items)

    orders_df.to_csv(
        OUTPUT_DIR / "orders.csv",
        index=False,
    )

    order_items_df.to_csv(
        OUTPUT_DIR / "order_items.csv",
        index=False,
    )

    print(f"Generated {len(orders_df)} orders")
    print(f"Generated {len(order_items_df)} order items")


if __name__ == "__main__":
    generate_orders()