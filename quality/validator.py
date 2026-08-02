from quality.checks import (
    validate_quantity,
    validate_price,
    validate_customer,
    validate_product,
)


def validate_record(record):

    errors = []

    if not validate_customer(record["customer_id"]):
        errors.append("Missing customer")

    if not validate_product(record["product_id"]):
        errors.append("Missing product")

    if not validate_quantity(record["quantity"]):
        errors.append("Invalid quantity")

    if not validate_price(record["price"]):
        errors.append("Invalid price")

    return errors