from config import db, app, bcrypt
from models import Store, Product, Request, User, SalesReport
from datetime import datetime

def seed_data():
    with app.app_context():
        # Clear existing data
        db.session.query(SalesReport).delete()
        db.session.query(Request).delete()
        db.session.query(Product).delete()
        db.session.query(Store).delete()
        db.session.query(User).delete()
        db.session.commit()

        # Create Users
        admin1 = User(username="admin1", email="admin1@example.com", role="admin")
        clerk1 = User(username="clerk1", email="clerk1@example.com", role="clerk")
        admin2 = User(username="admin2", email="admin2@example.com", role="admin")

        # Set passwords
        admin1.password_hash = "adminpassword"
        clerk1.password_hash = "clerkpassword"
        admin2.password_hash = "adminpassword2"

        db.session.add_all([admin1, clerk1, admin2])
        db.session.commit()

        # Create Stores
        store1 = Store(name="Store 1", location="Location 1", admin_id=admin1.id)
        store2 = Store(name="Store 2", location="Location 2", admin_id=admin2.id)

        db.session.add_all([store1, store2])
        db.session.commit()

        # Update User's store_id
        admin1.store_id = store1.id
        clerk1.store_id = store1.id
        admin2.store_id = store2.id

        db.session.add_all([admin1, clerk1, admin2])
        db.session.commit()

        # Create Products
        product1 = Product(
            brand_name="Brand A",
            product_name="Product 1",
            availability=True,
            payment_status="Paid",
            received_items=10,
            closing_stock=100,
            spoilt_items=0,
            buying_price=100.0,
            selling_price=150.0,
            store_id=store1.id
        )
        product2 = Product(
            brand_name="Brand B",
            product_name="Product 2",
            availability=False,
            payment_status="Unpaid",
            received_items=5,
            closing_stock=50,
            spoilt_items=0,
            buying_price=200.0,
            selling_price=250.0,
            store_id=store2.id
        )

        db.session.add_all([product1, product2])
        db.session.commit()

        # Create Requests
        request1 = Request(description="Request 1", product_id=product1.id, clerk_id=clerk1.id, admin_id=admin1.id, store_id=store1.id)
        request2 = Request(description="Request 2", product_id=product2.id, clerk_id=clerk1.id, admin_id=admin2.id, store_id=store2.id)

        db.session.add_all([request1, request2])
        db.session.commit()

        # Create Sales Reports
        sales_report1 = SalesReport(
            date=datetime.now(),
            product_id=product1.id,
            product_name=product1.product_name,
            store_id=store1.id,
            quantity_sold=10,
            quantity_in_hand=90,
            profit=500.0
        )
        sales_report2 = SalesReport(
            date=datetime.now(),
            product_id=product2.id,
            product_name=product2.product_name,
            store_id=store2.id,
            quantity_sold=5,
            quantity_in_hand=45,
            profit=250.0        
        )

        db.session.add_all([sales_report1, sales_report2])
        db.session.commit()

if __name__ == "__main__":
    seed_data()
