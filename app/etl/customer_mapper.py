from app.models.customer import Customer


class CustomerMapper:

    @staticmethod
    def map(df):

        customers = []

        for _, row in df.iterrows():

            customers.append(

                Customer(

                    customer_id=int(row.customer_id),

                    first_name=row.first_name,

                    last_name=row.last_name,

                    email=row.email,

                    phone=row.phone,

                    city=row.city,

                    state=row.state,

                    created_at=row.created_at,

                )

            )

        return customers