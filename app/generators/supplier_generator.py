from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker()

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_suppliers(num_suppliers=200):

    suppliers = []

    for supplier_id in range(1, num_suppliers + 1):

        suppliers.append(
            {
                "supplier_id": supplier_id,
                "supplier_name": fake.company(),
                "contact_name": fake.name(),
                "email": fake.unique.company_email(),
                "phone": fake.phone_number(),
                "city": fake.city(),
                "state": fake.state_abbr(),
            }
        )

    df = pd.DataFrame(suppliers)

    output_file = OUTPUT_DIR / "suppliers.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} suppliers")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    generate_suppliers()