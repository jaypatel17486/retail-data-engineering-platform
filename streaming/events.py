import random
import uuid
from datetime import datetime, timezone

from faker import Faker


fake = Faker()


def current_timestamp():
    return datetime.now(timezone.utc).isoformat()


def generate_event_id():
    return f"evt_{uuid.uuid4().hex[:12]}"


def generate_order_id():
    return f"ORD-{random.randint(100000, 999999)}"


def generate_customer_id():
    return f"CUS-{random.randint(1, 1000):04d}"


def generate_order_created_event():
    quantity = random.randint(1, 5)
    unit_price = round(random.uniform(5, 250), 2)
    total_amount = round(quantity * unit_price, 2)

    return {
        "event_id": generate_event_id(),
        "event_type": "order_created",
        "order_id": generate_order_id(),
        "customer_id": generate_customer_id(),
        "product_id": f"PROD-{random.randint(1, 100):04d}",
        "quantity": quantity,
        "unit_price": unit_price,
        "total_amount": total_amount,
        "currency": "USD",
        "timestamp": current_timestamp(),
    }


def generate_transaction():
    """
    Generate a realistic FluxGuard transaction.

    Transaction profiles:
    - Normal
    - Suspicious/Fraud
    - Failed

    is_fraud is synthetic ground truth for future ML training.
    """

    order = generate_order_created_event()

    # -----------------------------------------------------
    # CHOOSE TRANSACTION PROFILE
    # -----------------------------------------------------

    profile = random.choices(
        ["normal", "fraud", "failed"],
        weights=[80, 15, 5],
        k=1,
    )[0]

    # Start with same billing/shipping country
    billing_country = fake.country_code()
    shipping_country = billing_country

    payment = {
        "event_id": generate_event_id(),
        "order_id": order["order_id"],
        "customer_id": order["customer_id"],
        "amount": order["total_amount"],
        "currency": order["currency"],
        "payment_method": random.choice(
            [
                "credit_card",
                "debit_card",
                "paypal",
            ]
        ),
        "device_id": f"DEV-{random.randint(1000, 9999)}",
        "ip_address": fake.ipv4_public(),
        "billing_country": billing_country,
        "shipping_country": shipping_country,
        "timestamp": current_timestamp(),
    }

    # -----------------------------------------------------
    # NORMAL TRANSACTION
    # -----------------------------------------------------

    if profile == "normal":

        payment["event_type"] = "payment_completed"
        payment["is_fraud"] = 0
        payment["transaction_profile"] = "normal"

    # -----------------------------------------------------
    # SYNTHETIC FRAUD TRANSACTION
    # -----------------------------------------------------

    elif profile == "fraud":

        payment["event_type"] = "payment_completed"
        payment["is_fraud"] = 1
        payment["transaction_profile"] = "fraud"

        # Fraud transactions tend to have larger amounts
        fraud_amount = round(
            random.uniform(1000, 2500),
            2
        )

        payment["amount"] = fraud_amount
        order["total_amount"] = fraud_amount

        # Frequently create country mismatch
        if random.random() < 0.80:
            new_country = fake.country_code()

            while new_country == billing_country:
                new_country = fake.country_code()

            payment["shipping_country"] = new_country

    # -----------------------------------------------------
    # FAILED PAYMENT
    # -----------------------------------------------------

    else:

        payment["event_type"] = "payment_failed"
        payment["transaction_profile"] = "failed"

        failure_reason = random.choice(
            [
                "insufficient_funds",
                "incorrect_card_details",
                "expired_card",
                "payment_declined",
                "suspected_fraud",
            ]
        )

        payment["failure_reason"] = failure_reason

        # A failed payment isn't automatically fraud.
        if failure_reason == "suspected_fraud":
            payment["is_fraud"] = 1
        else:
            payment["is_fraud"] = 0

    return order, payment


# Keep old code compatible temporarily
def generate_order_event():
    return generate_order_created_event()