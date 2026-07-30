from pathlib import Path
import pandas as pd

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_categories():

    categories = [
        {"category_id": 1, "category_name": "Electronics"},
        {"category_id": 2, "category_name": "Home"},
        {"category_id": 3, "category_name": "Sports"},
        {"category_id": 4, "category_name": "Books"},
        {"category_id": 5, "category_name": "Clothing"},
        {"category_id": 6, "category_name": "Health"},
        {"category_id": 7, "category_name": "Beauty"},
        {"category_id": 8, "category_name": "Toys"},
        {"category_id": 9, "category_name": "Furniture"},
        {"category_id": 10, "category_name": "Groceries"},
    ]

    df = pd.DataFrame(categories)

    output_file = OUTPUT_DIR / "categories.csv"

    df.to_csv(output_file, index=False)

    print(f"Generated {len(df)} categories")
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    generate_categories()