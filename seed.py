from config import db, app
from models import Store, Product, Request, User
from sqlalchemy.exc import IntegrityError

def seed_data():
    with app.app_context():
        # Clear existing data
        db.session.query(Request).delete()
        db.session.query(Product).delete()
        db.session.query(Store).delete()
        db.session.query(User).delete()

        # Add Users
        users = [
            User(username="admin", email="admin@example.com", _password_hash="adminpassword", role="admin"),
            User(username="clerk", email="clerk@example.com", _password_hash="clerkpassword", role="clerk"),
            User(username="admin2", email="admin2@example.com", _password_hash="adminpassword2", role="admin"),
        ]
        db.session.add_all(users)
        db.session.commit()

        # Add Stores
        stores = [
            Store(name="Store 1", location="Location 1", admin_id=users[0].id),
            Store(name="Store 2", location="Location 2", admin_id=users[2].id)
        ]
        db.session.add_all(stores)
        db.session.commit()

        # Update user store_id for clerks
        users[1].store_id = stores[0].id
        db.session.commit()

        # Add Products
        products = [
            Product(brand_name="Brand A", product_name="Product 1", availability=True, payment_status="Paid", closing_stock=10, buying_price=100.0, selling_price=150.0, store_id=stores[0].id),
            Product(brand_name="Brand B", product_name="Product 2", availability=False, payment_status="Unpaid", closing_stock=5, buying_price=200.0, selling_price=250.0, store_id=stores[1].id)
        ]
        db.session.add_all(products)
        db.session.commit()

        # Add Requests
        requests = [
            Request(description="Request 1", product_id=products[0].id, clerk_id=users[1].id, admin_id=users[0].id),
            Request(description="Request 2", product_id=products[1].id, clerk_id=users[1].id, admin_id=users[2].id)
        ]
        db.session.add_all(requests)
        db.session.commit()

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            print("There was an error seeding the database.")

if __name__ == "__main__":
    seed_data()
