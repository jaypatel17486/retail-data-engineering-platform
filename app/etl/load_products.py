from app.services.product_service import ProductService


def main():

    ProductService().load_products()


if __name__ == "__main__":
    main()