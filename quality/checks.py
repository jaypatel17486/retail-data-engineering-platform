def validate_quantity(quantity):
    return quantity > 0


def validate_price(price):
    return price >= 0


def validate_customer(customer_id):
    return customer_id is not None


def validate_product(product_id):
    return product_id is not None