from pathlib import Path

import pandas as pd

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_stores():

    stores = [
        {"store_id": 1, "store_name": "Los Angeles Store", "city": "Los Angeles", "state": "CA"},
        {"store_id": 2, "store_name": "San Francisco Store", "city": "San Francisco", "state": "CA"},
        {"store_id": 3, "store_name": "New York Store", "city": "New York", "state": "NY"},
        {"store_id": 4, "store_name": "Chicago Store", "city": "Chicago", "state": "IL"},
        {"store_id": 5, "store_name": "Dallas Store", "city": "Dallas", "state": "TX"},
        {"store_id": 6, "store_name": "Houston Store", "city": "Houston", "state": "TX"},
        {"store_id": 7, "store_name": "Seattle Store", "city": "Seattle", "state": "WA"},
        {"store_id": 8, "store_name": "Boston Store", "city": "Boston", "state": "MA"},
        {"store_id": 9, "store_name": "Miami Store", "city": "Miami", "state": "FL"},
        {"store_id": 10, "store_name": "Phoenix Store", "city": "Phoenix", "state": "AZ"},
    ]

    df = pd.DataFrame(stores)

    output_file = OUTPUT_DIR / "stores.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} stores")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    generate_stores()