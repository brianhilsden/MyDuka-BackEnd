from datetime import datetime
from config import db, app, bcrypt
from models import Store, Product, Request, Merchant, Admin, Clerk, SalesReport

def seed_data():
    with app.app_context():
        # Clear existing data
        db.session.query(SalesReport).delete()
        db.session.query(Request).delete()
        db.session.query(Product).delete()
        db.session.query(Clerk).delete()
        db.session.query(Admin).delete()
        db.session.query(Merchant).delete()
        db.session.query(Store).delete()
        db.session.commit()

        # Create Stores
        store1 = Store(name="Store A", location="Nairobi")
        store2 = Store(name="Store B", location="Mombasa")

        db.session.add_all([store1, store2])
        db.session.commit()

        # Create Merchants
        merchant1 = Merchant(username="merchant1", email="merchant1@example.com", store_id=store1.id)
        merchant2 = Merchant(username="merchant2", email="merchant2@example.com", store_id=store2.id)

        merchant1.password_hash = "merchantpassword1"
        merchant2.password_hash = "merchantpassword2"

        db.session.add_all([merchant1, merchant2])
        db.session.commit()

        # Create Admins
        admin1 = Admin(username="admin1", email="admin1@example.com", store_id=store1.id, role="manager")
        admin2 = Admin(username="admin2", email="admin2@example.com", store_id=store2.id, role="manager")

        admin1.password_hash = "adminpassword1"
        admin2.password_hash = "adminpassword2"

        db.session.add_all([admin1, admin2])
        db.session.commit()

        # Create Clerks
        clerk1 = Clerk(username="clerk1", email="clerk1@example.com", store_id=store1.id, role="sales")
        clerk2 = Clerk(username="clerk2", email="clerk2@example.com", store_id=store2.id, role="sales")

        clerk1.password_hash = "clerkpassword1"
        clerk2.password_hash = "clerkpassword2"

        db.session.add_all([clerk1, clerk2])
        db.session.commit()

        # Create Products
        product1 = Product(
            brand_name="Brand X",
            product_name="Product X",
            availability=True,
            payment_status="paid",
            received_items=20,
            closing_stock=15,
            spoilt_items=1,
            buying_price=150.0,
            selling_price=200.0,
            store_id=store1.id
        )
        product2 = Product(
            brand_name="Brand Y",
            product_name="Product Y",
            availability=True,
            payment_status="unpaid",
            received_items=30,
            closing_stock=25,
            spoilt_items=2,
            buying_price=100.0,
            selling_price=140.0,
            store_id=store2.id
        )

        db.session.add_all([product1, product2])
        db.session.commit()

        # Create Requests
        request1 = Request(
            date=datetime.now(),
            description="Restock Product X",
            quantity=10,
            product_id=product1.id,
            clerk_id=clerk1.id,
            admin_id=admin1.id,
            store_id=store1.id
        )
        request2 = Request(
            date=datetime.now(),
            description="Restock Product Y",
            quantity=15,
            product_id=product2.id,
            clerk_id=clerk2.id,
            admin_id=admin2.id,
            store_id=store2.id
        )

        db.session.add_all([request1, request2])
        db.session.commit()

        # Create Sales Reports
        sales_report1 = SalesReport(
            date=datetime.now(),
            product_name=product1.product_name,
            product_id=product1.id,
            store_id=store1.id,
            quantity_sold=5,
            quantity_in_hand=10,
            profit=250.0
        )
        sales_report2 = SalesReport(
            date=datetime.now(),
            product_name=product2.product_name,
            product_id=product2.id,
            store_id=store2.id,
            quantity_sold=10,
            quantity_in_hand=15,
            profit=400.0
        )

        db.session.add_all([sales_report1, sales_report2])
        db.session.commit()

if __name__ == "__main__":
    seed_data()
