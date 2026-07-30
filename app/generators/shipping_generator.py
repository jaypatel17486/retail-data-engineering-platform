from pathlib import Path
import random

import pandas as pd
from faker import Faker

fake = Faker()

OUTPUT_DIR = Path("data/raw")

orders = pd.read_csv(OUTPUT_DIR / "orders.csv")


def generate_shipping():

    shipping = []

    carriers = [
        "UPS",
        "FedEx",
        "USPS",
        "DHL",
        "Amazon Logistics",
    ]

    for _, order in orders.iterrows():

        shipping_date = fake.date_time_between(
            start_date="-1y",
            end_date="now",
        )

        delivery_date = fake.date_time_between(
            start_date=shipping_date,
            end_date="+7d",
        )

        shipping.append(
            {
                "shipping_id": int(order["order_id"]),
                "order_id": int(order["order_id"]),
                "carrier": random.choice(carriers),
                "tracking_number": fake.uuid4(),
                "shipping_date": shipping_date,
                "delivery_date": delivery_date,
            }
        )

    df = pd.DataFrame(shipping)

    output_file = OUTPUT_DIR / "shipping.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} shipping records")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    generate_shipping()