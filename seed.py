from datetime import datetime, timedelta
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
        db.session.query(Store).delete()
        db.session.query(Merchant).delete()
      
        db.session.commit()

        # Create Merchants
        merchant1 = Merchant(username="Ryan", email="ryan@gmail.com", role="Merchant")
        merchant1.password_hash = "ryanpassword"
        db.session.add(merchant1)
        db.session.commit()

        # Create Stores
        store1 = Store(name="Store A", location="Nairobi", merchant_id=merchant1.id)
        store2 = Store(name="Store B", location="Mombasa", merchant_id=merchant1.id)
        store3 = Store(name="Store C", location="Kisumu", merchant_id=merchant1.id)
        db.session.add_all([store1, store2, store3])
        db.session.commit()

        # Create Admins
        admin1 = Admin(username="Carlson", email="carlson@gmail.com", store_id=store1.id, role="Admin")
        admin2 = Admin(username="Michelle", email="michelle@gmail.com", store_id=store2.id, role="Admin")
        admin1.password_hash = "carlsonpassword"
        admin2.password_hash = "michellepassword"
        db.session.add_all([admin1, admin2])
        db.session.commit()

        # Create Clerks
        clerk1 = Clerk(username="Grace", email="grace@gmail.com", store_id=store1.id, role="Clerk")
        clerk2 = Clerk(username="Simon", email="simon@gmail.com", store_id=store2.id, role="Clerk")
        clerk3 = Clerk(username="Tony", email="tony@gmail.com", store_id=store1.id, role="Clerk")
        clerk1.password_hash = "gracepassword"
        clerk2.password_hash = "simonpassword"
        clerk3.password_hash = "tonypassword"
        db.session.add_all([clerk1, clerk2, clerk3])
        db.session.commit()

        # Create Products
        product1 = Product(
            brand_name="Pishori",
            product_name="Rice",
            availability=True,
            payment_status="paid",
            received_items=100,
            closing_stock=100,
            spoilt_items=10,
            buying_price=121.0,
            selling_price=150.0,
            store_id=store1.id
        )
        product2 = Product(
            brand_name="Yellow",
            product_name="Beans",
            availability=True,
            payment_status="unpaid",
            received_items=100,
            closing_stock=100,
            spoilt_items=0,
            buying_price=143.0,
            selling_price=180.0,
            store_id=store1.id
        )
        product3 = Product(
            brand_name="Butterfly Grains",
            product_name="Green Grams",
            availability=True,
            payment_status="unpaid",
            received_items=100,
            closing_stock=100,
            spoilt_items=2,
            buying_price=121.0,
            selling_price=140.0,
            store_id=store1.id
        )
        product4 = Product(
            brand_name="Golden",
            product_name="Maize Flour",
            availability=True,
            payment_status="paid",
            received_items=100,
            closing_stock=100,
            spoilt_items=5,
            buying_price=100.0,
            selling_price=120.0,
            store_id=store2.id
        )
        product5 = Product(
            brand_name="DairyBest",
            product_name="Milk",
            availability=True,
            payment_status="unpaid",
            received_items=100,
            closing_stock=100,
            spoilt_items=0,
            buying_price=50.0,
            selling_price=60.0,
            store_id=store2.id
        )
        product6 = Product(
            brand_name="SweetFarm",
            product_name="Honey",
            availability=True,
            payment_status="unpaid",
            received_items=100,
            closing_stock=100,
            spoilt_items=1,
            buying_price=200.0,
            selling_price=250.0,
            store_id=store2.id
        )
        product7 = Product(
            brand_name="NutriLife",
            product_name="Peanut Butter",
            availability=True,
            payment_status="paid",
            received_items=100,
            closing_stock=100,
            spoilt_items=0,
            buying_price=150.0,
            selling_price=175.0,
            store_id=store3.id
        )
        product8 = Product(
            brand_name="Nature's Gold",
            product_name="Oats",
            availability=True,
            payment_status="unpaid",
            received_items=100,
            closing_stock=100,
            spoilt_items=2,
            buying_price=80.0,
            selling_price=100.0,
            store_id=store3.id
        )
        product9 = Product(
            brand_name="GreenFarm",
            product_name="Spinach",
            availability=True,
            payment_status="unpaid",
            received_items=100,
            closing_stock=100,
            spoilt_items=3,
            buying_price=30.0,
            selling_price=40.0,
            store_id=store3.id
        )
        db.session.add_all([product1, product2, product3, product4, product5, product6, product7, product8, product9])
        db.session.commit()

        # Create Requests (Restocks)
        request1 = Request(
            date=datetime.now() - timedelta(days=2),
            description="Restock Rice",
            quantity=50,
            product_id=product1.id,
            clerk_id=clerk1.id,
            admin_id=admin1.id,
            store_id=store1.id
        )
        product1.closing_stock += request1.quantity

        request2 = Request(
            date=datetime.now() - timedelta(days=3),
            description="Restock Beans",
            quantity=30,
            product_id=product2.id,
            clerk_id=clerk3.id,
            admin_id=admin1.id,
            store_id=store1.id
        )
        product2.closing_stock += request2.quantity

        db.session.add_all([request1, request2])
        db.session.commit()

        # Create Sales Reports for Store 1
        sales_report1 = SalesReport(
            date=datetime.now(),
            product_name=product1.product_name,
            product_id=product1.id,
            store_id=store1.id,
            quantity_sold=10,
            quantity_in_hand=product1.closing_stock - 10,
            profit=10 * (product1.selling_price - product1.buying_price),
            clerk_id=clerk3.id
        )
        product1.closing_stock = sales_report1.quantity_in_hand

        sales_report2 = SalesReport(
            date=datetime.now() - timedelta(days=1),
            product_name=product1.product_name,
            product_id=product1.id,
            store_id=store1.id,
            quantity_sold=15,
            quantity_in_hand=product1.closing_stock - 15,
            profit=15 * (product1.selling_price - product1.buying_price),
            clerk_id=clerk1.id
        )
        product1.closing_stock = sales_report2.quantity_in_hand

        sales_report3 = SalesReport(
            date=datetime.now() - timedelta(days=2),
            product_name=product1.product_name,
            product_id=product1.id,
            store_id=store1.id,
            quantity_sold=20,
            quantity_in_hand=product1.closing_stock - 20,
            profit=20 * (product1.selling_price - product1.buying_price),
            clerk_id=clerk3.id
        )
        product1.closing_stock = sales_report3.quantity_in_hand

        sales_report4 = SalesReport(
            date=datetime.now() - timedelta(days=3),
            product_name=product2.product_name,
            product_id=product2.id,
            store_id=store1.id,
            quantity_sold=11,
            quantity_in_hand=product2.closing_stock - 11,
            profit=11 * (product2.selling_price - product2.buying_price),
            clerk_id=clerk1.id
        )
        product2.closing_stock = sales_report4.quantity_in_hand

        sales_report5 = SalesReport(
            date=datetime.now() - timedelta(days=4),
            product_name=product2.product_name,
            product_id=product2.id,
            store_id=store1.id,
            quantity_sold=13,
            quantity_in_hand=product2.closing_stock - 13,
            profit=13 * (product2.selling_price - product2.buying_price),
            clerk_id=clerk1.id
        )
        product2.closing_stock = sales_report5.quantity_in_hand

        db.session.add_all([sales_report1, sales_report2, sales_report3, sales_report4, sales_report5])
        db.session.commit()

if __name__ == "__main__":
    seed_data()
