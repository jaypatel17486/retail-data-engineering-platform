from app.generators.category_generator import generate_categories
from app.generators.supplier_generator import generate_suppliers
from app.generators.store_generator import generate_stores
from app.generators.customer_generator import generate_customers
from app.generators.product_generator import generate_products
from app.generators.order_generator import generate_orders
from app.generators.payment_generator import generate_payments
from app.generators.shipping_generator import generate_shipping
from app.generators.inventory_generator import generate_inventory


def main():

    print("Generating Categories...")
    generate_categories()

    print("Generating Suppliers...")
    generate_suppliers()

    print("Generating Stores...")
    generate_stores()

    print("Generating Customers...")
    generate_customers()

    print("Generating Products...")
    generate_products()

    print("Generating Orders...")
    generate_orders()

    print("Generating Payments...")
    generate_payments()

    print("Generating Shipping...")
    generate_shipping()

    print("Generating Inventory...")
    generate_inventory()

    print("\nAll datasets generated successfully!")


if __name__ == "__main__":
    main()