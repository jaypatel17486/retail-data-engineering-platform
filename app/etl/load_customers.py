from app.services.customer_service import CustomerService


def main():
    service = CustomerService()
    service.load_customers()


if __name__ == "__main__":
    main()