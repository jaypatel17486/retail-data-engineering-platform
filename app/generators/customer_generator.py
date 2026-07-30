from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker()

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_customers(num_customers=1000):

    customers = []

    for customer_id in range(1, num_customers + 1):

        customers.append(
            {
                "customer_id": customer_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.unique.email(),
                "phone": fake.phone_number(),
                "city": fake.city(),
                "state": fake.state_abbr(),
                "created_at": fake.date_time_between(
                    start_date="-2y",
                    end_date="now",
                ),
            }
        )

    df = pd.DataFrame(customers)

    output_file = OUTPUT_DIR / "customers.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} customers")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    generate_customers()