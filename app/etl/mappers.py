from app.models import (
    Category,
    Supplier,
    Store,
    Customer,
    Product,
    Inventory,
    Order,
    OrderItem,
    Payment,
    Shipping,
)

MODEL_MAP = {
    "categories": Category,
    "suppliers": Supplier,
    "stores": Store,
    "customers": Customer,
    "products": Product,
    "inventory": Inventory,
    "orders": Order,
    "order_items": OrderItem,
    "payments": Payment,
    "shipping": Shipping,
}