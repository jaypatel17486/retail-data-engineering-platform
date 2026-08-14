import os

import pandas as pd

from streaming.events import generate_transaction


DATASET_PATH = "fraud/ml/transactions.csv"


def transaction_to_features(payment):
    """
    Convert a payment event into ML-friendly features.
    """

    return {
        "amount": float(payment["amount"]),

        "country_mismatch": int(
            payment.get("billing_country")
            != payment.get("shipping_country")
        ),

        "payment_failed": int(
            payment["event_type"] == "payment_failed"
        ),

        "suspected_fraud_failure": int(
            payment.get("failure_reason") == "suspected_fraud"
        ),

        # Target label
        "is_fraud": int(payment["is_fraud"]),
    }


def generate_dataset(num_transactions=10000):

    rows = []

    print(
        f"Generating {num_transactions:,} "
        "FluxGuard transactions..."
    )

    for _ in range(num_transactions):

        _, payment = generate_transaction()

        rows.append(
            transaction_to_features(payment)
        )

    dataframe = pd.DataFrame(rows)

    os.makedirs(
        os.path.dirname(DATASET_PATH),
        exist_ok=True,
    )

    dataframe.to_csv(
        DATASET_PATH,
        index=False,
    )

    print()
    print("Dataset created successfully.")
    print(f"Location: {DATASET_PATH}")
    print(f"Rows: {len(dataframe):,}")

    print()
    print("Fraud distribution:")
    print(
        dataframe["is_fraud"]
        .value_counts()
        .sort_index()
    )

    print()
    print(dataframe.head())


if __name__ == "__main__":
    generate_dataset()