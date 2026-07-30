from app.models.category import Category
from app.models.supplier import Supplier
from app.models.store import Store
from app.models.customer import Customer
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.shipping import Shipping

PIPELINE_TABLES = [
    ("categories.csv", Category),
    ("suppliers.csv", Supplier),
    ("stores.csv", Store),
    ("customers.csv", Customer),
    ("products.csv", Product),
    ("inventory.csv", Inventory),
    ("orders.csv", Order),
    ("order_items.csv", OrderItem),
    ("payments.csv", Payment),
    ("shipping.csv", Shipping),
]