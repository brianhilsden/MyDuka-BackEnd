from datetime import datetime,timedelta
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
        merchant1 = Merchant(username="merchant1", email="merchant1@example.com",role="Merchant")
        

        merchant1.password_hash = "merchantpassword1"
      

        db.session.add(merchant1)
        db.session.commit()


        # Create Stores
        store1 = Store(name="Store A", location="Nairobi",merchant_id=merchant1.id)
        store2 = Store(name="Store B", location="Mombasa",merchant_id=merchant1.id)
        store3 = Store(name="Store C", location="Kisumu",merchant_id=merchant1.id)

        db.session.add_all([store1, store2,store3])
        db.session.commit()

      
        # Create Admins
        admin1 = Admin(username="admin1", email="admin1@example.com", store_id=store1.id, role="Admin")
        admin2 = Admin(username="admin2", email="admin2@example.com", store_id=store2.id, role="Admin")

        admin1.password_hash = "adminpassword1"
        admin2.password_hash = "adminpassword2"

        db.session.add_all([admin1, admin2])
        db.session.commit()

        # Create Clerks
        clerk1 = Clerk(username="Grace", email="grace@gmail.com", store_id=store1.id, role="Clerk")
        clerk2 = Clerk(username="Simon", email="simon@gmail.com", store_id=store2.id, role="Clerk")
        clerk3 = Clerk(username="Tony", email="tony@gmail.com", store_id=store1.id, role="Clerk")

        clerk1.password_hash = "gracepassword"
        clerk2.password_hash = "clerkpassword2"
        clerk3.password_hash = "tonypassword"

        db.session.add_all([clerk1, clerk2,clerk3])
        db.session.commit()
               
         # Create Products
        product1 = Product(
                    brand_name="Pishori",
                    product_name="Rice",
                    availability=True,
                    payment_status="paid",
                    received_items=10,
                    closing_stock=15,
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
                    received_items=45,
                    closing_stock=45,
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
                    received_items=43,
                    closing_stock=10,
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
                    received_items=30,
                    closing_stock=20,
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
                    received_items=50,
                    closing_stock=50,
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
                    received_items=25,
                    closing_stock=25,
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
                    received_items=60,
                    closing_stock=50,
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
                    received_items=20,
                    closing_stock=20,
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
                    received_items=40,
                    closing_stock=40,
                    spoilt_items=3,
                    buying_price=30.0,
                    selling_price=40.0,
                    store_id=store3.id
                )

        db.session.add_all([product1, product2, product3, product4, product5, product6, product7, product8, product9])
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
            clerk_id=clerk3.id,
            admin_id=admin1.id,
            store_id=store1.id
        )

        db.session.add_all([request1, request2])
        db.session.commit()

        # Create Sales Reports
        sales_report1 = SalesReport(
            date=datetime.now(),
            product_name=product1.product_name,
            product_id=product1.id,
            store_id=store1.id,
            quantity_sold=10,
            quantity_in_hand=82,
            profit=360.0,
            clerk_id = clerk3.id
        )
        sales_report2 = SalesReport(
            date=datetime.now() - timedelta(days=1),
            product_name=product1.product_name,
            product_id=product1.id,
            store_id=store1.id,
            quantity_sold=15,
            quantity_in_hand=67,
            profit=300.0,
            clerk_id = clerk1.id
        )
        sales_report3 = SalesReport(
            date=datetime.now() - timedelta(days=2),
            product_name=product1.product_name,
            product_id=product1.id,
            store_id=store1.id,
            quantity_sold=20,
            quantity_in_hand=47,
            profit=400.0,
            clerk_id = clerk3.id
        )
        sales_report4 = SalesReport(
            date=datetime.now() - timedelta(days=3),
            product_name=product2.product_name,
            product_id=product2.id,
            store_id=store1.id,
            quantity_sold=11,
            quantity_in_hand=39,
            profit=220.0,
            clerk_id = clerk1.id
        )
        sales_report5 = SalesReport(
            date=datetime.now() - timedelta(days=4),
            product_name=product2.product_name,
            product_id=product2.id,
            store_id=store1.id,
            quantity_sold=13,
            quantity_in_hand=2,
            profit=260.0,
            clerk_id = clerk3.id
        )
        sales_report6 = SalesReport(
            date=datetime.now() - timedelta(days=5  ),
            product_name=product2.product_name,
            product_id=product2.id,
            store_id=store1.id,
            quantity_sold=16,
            quantity_in_hand=10,
            profit=320.0,
            clerk_id = clerk1.id
        )
        sales_report7 = SalesReport(
            date=datetime.now() - timedelta(days=6),
            product_name=product3.product_name,
            product_id=product3.id,
            store_id=store1.id,
            quantity_sold=15,
            quantity_in_hand=35,
            profit=300.0,
            clerk_id = clerk3.id
        )
        sales_report8 = SalesReport(
            date=datetime.now() - timedelta(days=7),
            product_name=product3.product_name,
            product_id=product3.id,
            store_id=store1.id,
            quantity_sold=18,
            quantity_in_hand=17,
            profit=360.0,
            clerk_id = clerk1.id
        )
        sales_report9 = SalesReport(
            date=datetime.now() - timedelta(days=8),
            product_name=product3.product_name,
            product_id=product3.id,
            store_id=store1.id,
            quantity_sold=12,
            quantity_in_hand=5,
            profit=240.0,
            clerk_id = clerk3.id
        )
          # Create Sales Reports for Store 2
        sales_report10 = SalesReport(
                    date=datetime.now(),
                    product_name=product4.product_name,
                    product_id=product4.id,
                    store_id=store2.id,
                    quantity_sold=10,
                    quantity_in_hand=20,
                    profit=200.0,
                    clerk_id = clerk2.id
                )
        sales_report11 = SalesReport(
                    date=datetime.now() - timedelta(days=1),
                    product_name=product4.product_name,
                    product_id=product4.id,
                    store_id=store2.id,
                    quantity_sold=12,
                    quantity_in_hand=8,
                    profit=240.0,
                    clerk_id = clerk2.id
                )
        sales_report12 = SalesReport(
                    date=datetime.now() - timedelta(days=2),
                    product_name=product5.product_name,
                    product_id=product5.id,
                    store_id=store2.id,
                    quantity_sold=20,
                    quantity_in_hand=30,
                    profit=400.0,
                    clerk_id = clerk2.id
                )
        sales_report13 = SalesReport(
                    date=datetime.now() - timedelta(days=3),
                    product_name=product5.product_name,
                    product_id=product5.id,
                    store_id=store2.id,
                    quantity_sold=15,
                    quantity_in_hand=35,
                    profit=300.0,
                    clerk_id = clerk2.id
                )
        sales_report14 = SalesReport(
                    date=datetime.now() - timedelta(days=4),
                    product_name=product6.product_name,
                    product_id=product6.id,
                    store_id=store2.id,
                    quantity_sold=16,
                    quantity_in_hand=24,
                    profit=320.0,
                    clerk_id = clerk2.id
                )
        sales_report15 = SalesReport(
                    date=datetime.now() - timedelta(days=5),
                    product_name=product6.product_name,
                    product_id=product6.id,
                    store_id=store2.id,
                    quantity_sold=18,
                    quantity_in_hand=7,
                    profit=360.0,
                    clerk_id = clerk2.id
                )

        db.session.add_all([sales_report1, sales_report2, sales_report3, sales_report4, sales_report5, sales_report6, sales_report7, sales_report8, sales_report9,sales_report10,sales_report11,sales_report12,sales_report13,sales_report14,sales_report15])
        db.session.commit()

if __name__ == "__main__":

    seed_data()
