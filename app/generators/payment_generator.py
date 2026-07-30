from pathlib import Path
import random

import pandas as pd
from faker import Faker

fake = Faker()

OUTPUT_DIR = Path("data/raw")

orders = pd.read_csv(OUTPUT_DIR / "orders.csv")
order_items = pd.read_csv(OUTPUT_DIR / "order_items.csv")


def generate_payments():

    payments = []

    payment_methods = [
        "Credit Card",
        "Debit Card",
        "PayPal",
        "Apple Pay",
        "Google Pay",
    ]

    for _, order in orders.iterrows():

        items = order_items[
            order_items["order_id"] == order["order_id"]
        ]

        total_amount = (
            items["quantity"] * items["unit_price"]
        ).sum()

        payments.append(
            {
                "payment_id": int(order["order_id"]),
                "order_id": int(order["order_id"]),
                "payment_method": random.choice(payment_methods),
                "amount": round(total_amount, 2),
                "payment_date": fake.date_time_between(
                    start_date="-1y",
                    end_date="now"
                ),
            }
        )

    df = pd.DataFrame(payments)

    output_file = OUTPUT_DIR / "payments.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} payments")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    generate_payments()