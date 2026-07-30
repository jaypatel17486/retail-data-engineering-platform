from app.database.database import SessionLocal
from app.models.streaming_order import StreamingOrder


class StreamingRepository:

    def __init__(self):
        self.db = SessionLocal()

    def save(self, event):

        order = StreamingOrder(
            order_id=event["order_id"],
            customer_id=event["customer_id"],
            product_id=event["product_id"],
            quantity=event["quantity"],
            price=event["price"],
            payment_method=event["payment_method"],
            status=event["status"],
            timestamp=event["timestamp"],
        )

        self.db.add(order)
        self.db.commit()

    def close(self):
        self.db.close()