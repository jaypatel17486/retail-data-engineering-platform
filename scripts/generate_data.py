from faker import Faker
import pandas as pd
import random
from pathlib import Path

fake = Faker()

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

customers = []

for customer_id in range(1, 1001):
    customers.append({
        "customer_id": customer_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.unique.email(),
        "phone": fake.phone_number(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "created_at": fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )
    })

df = pd.DataFrame(customers)

output_file = OUTPUT_DIR / "customers.csv"
df.to_csv(output_file, index=False)

print(f"Generated {len(df)} customers")
print(f"Saved to {output_file}")