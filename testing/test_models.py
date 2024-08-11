import unittest
from datetime import datetime
from test_config import app, db
from test_models import Merchant, Admin, Clerk, Store, Product, Request, SalesReport

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        cls.app = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def test_merchant_creation(self):
        with app.app_context():
            store = Store(name="Test Store", location="Test Location")
            db.session.add(store)
            db.session.commit()

            merchant = Merchant(username="test_merchant", email="merchant@test.com", store_id=store.id)
            merchant.password_hash = "password123"

            db.session.add(merchant)
            db.session.commit()

            retrieved_merchant = Merchant.query.filter_by(email="merchant@test.com").first()
            self.assertIsNotNone(retrieved_merchant)
            self.assertEqual(retrieved_merchant.username, "test_merchant")
            self.assertTrue(retrieved_merchant.verify_password("password123"))

    def test_admin_creation(self):
        with app.app_context():
            store = Store(name="Test Store", location="Test Location")
            db.session.add(store)
            db.session.commit()

            admin = Admin(username="test_admin", email="admin@test.com", store_id=store.id, role="admin")
            admin.password_hash = "adminpassword"

            db.session.add(admin)
            db.session.commit()

            retrieved_admin = Admin.query.filter_by(email="admin@test.com").first()
            self.assertIsNotNone(retrieved_admin)
            self.assertEqual(retrieved_admin.username, "test_admin")
            self.assertTrue(retrieved_admin.verify_password("adminpassword"))

    def test_clerk_creation(self):
        with app.app_context():
            store = Store(name="Test Store", location="Test Location")
            db.session.add(store)
            db.session.commit()

            clerk = Clerk(username="test_clerk", email="clerk@test.com", store_id=store.id, role="clerk")
            clerk.password_hash = "clerkpassword"

            db.session.add(clerk)
            db.session.commit()

            retrieved_clerk = Clerk.query.filter_by(email="clerk@test.com").first()
            self.assertIsNotNone(retrieved_clerk)
            self.assertEqual(retrieved_clerk.username, "test_clerk")
            self.assertTrue(retrieved_clerk.verify_password("clerkpassword"))

    def test_store_creation(self):
        with app.app_context():
            store = Store(name="Test Store", location="Test Location")
            db.session.add(store)
            db.session.commit()

            retrieved_store = Store.query.filter_by(name="Test Store").first()
            self.assertIsNotNone(retrieved_store)
            self.assertEqual(retrieved_store.location, "Test Location")

    def test_product_creation(self):
        with app.app_context():
            store = Store(name="Test Store", location="Test Location")
            db.session.add(store)
            db.session.commit()

            product = Product(
                brand_name="Brand X",
                product_name="Product X",
                availability=True,
                payment_status="paid",
                received_items=20,
                closing_stock=15,
                spoilt_items=1,
                buying_price=150.0,
                selling_price=200.0,
                store_id=store.id
            )
            db.session.add(product)
            db.session.commit()

            retrieved_product = Product.query.filter_by(product_name="Product X").first()
            self.assertIsNotNone(retrieved_product)
            self.assertEqual(retrieved_product.brand_name, "Brand X")
            self.assertEqual(retrieved_product.closing_stock, 15)

   

    def test_request_creation(self):
        with app.app_context():
            store = Store(name="Test Store", location="Test Location")
            db.session.add(store)
            db.session.commit()

            clerk = Clerk(username="test_clerk", email="clerk@test.com", store_id=store.id, role="clerk")
            clerk.password_hash = "clerkpassword"
            db.session.add(clerk)
            db.session.commit()

            admin = Admin(username="test_admin", email="admin@test.com", store_id=store.id, role="admin")
            admin.password_hash = "adminpassword"
            db.session.add(admin)
            db.session.commit()

            product = Product(
                brand_name="Brand X",
                product_name="Product X",
                availability=True,
                payment_status="paid",
                received_items=20,
                closing_stock=15,
                spoilt_items=1,
                buying_price=150.0,
                selling_price=200.0,
                store_id=store.id
            )
            db.session.add(product)
            db.session.commit()

            # Use datetime object instead of string
            request = Request(
                date=datetime(2023, 10, 26),  # Use a datetime object here
                description="Restock Product X",
                quantity=10,
                product_id=product.id,
                clerk_id=clerk.id,
                admin_id=admin.id,
                store_id=store.id
            )
            db.session.add(request)
            db.session.commit()

            retrieved_request = Request.query.filter_by(description="Restock Product X").first()
            self.assertIsNotNone(retrieved_request)
            self.assertEqual(retrieved_request.quantity, 10)
            self.assertEqual(retrieved_request.product_id, product.id)


    def test_sales_report_creation(self):
        with app.app_context():
            store = Store(name="Test Store", location="Test Location")
            db.session.add(store)
            db.session.commit()

            product = Product(
                brand_name="Brand X",
                product_name="Product X",
                availability=True,
                payment_status="paid",
                received_items=20,
                closing_stock=15,
                spoilt_items=1,
                buying_price=150.0,
                selling_price=200.0,
                store_id=store.id
            )
            db.session.add(product)
            db.session.commit()

            sales_report = SalesReport(
                date=datetime(2023, 10, 26),
                product_name="Product X",
                product_id=product.id,
                store_id=store.id,
                quantity_sold=5,
                quantity_in_hand=10,
                profit=250.0
            )
            db.session.add(sales_report)
            db.session.commit()

            retrieved_sales_report = SalesReport.query.filter_by(product_name="Product X").first()
            self.assertIsNotNone(retrieved_sales_report)
            self.assertEqual(retrieved_sales_report.quantity_sold, 5)
            self.assertEqual(retrieved_sales_report.profit, 250.0)

if __name__ == '__main__':
    unittest.main()