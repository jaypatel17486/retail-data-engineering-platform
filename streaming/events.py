from faker import Faker
import random
from datetime import datetime

fake = Faker()

def generate_order_event():
    return {
        "order_id": random.randint(100000, 999999),
        "customer_id": random.randint(1, 1000),
        "product_id": random.randint(1, 40),
        "quantity": random.randint(1, 5),
        "price": round(random.uniform(5, 250), 2),
        "payment_method": random.choice(
            ["Credit Card", "Debit Card", "PayPal"]
        ),
        "status": random.choice(
            ["Pending", "Completed", "Cancelled"]
        ),
        "timestamp": datetime.utcnow().isoformat()
    }