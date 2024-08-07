import unittest
from models import Merchant,  Store, Product
from config import db, bcrypt
from app import app

class ValidationTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()

        # Create a test store
        self.store = Store(name="Test Store", location="Test Location")
        db.session.add(self.store)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        merchant = Merchant(username="testmerchant", email="merchant@example.com", store_id=self.store.id)
        merchant.password_hash = "password123"

        self.assertNotEqual(merchant._password_hash, "password123")
        self.assertTrue(bcrypt.check_password_hash(merchant._password_hash, "password123"))

    def test_email_uniqueness(self):
        merchant1 = Merchant(username="testmerchant1", email="merchant@example.com", store_id=self.store.id)
        db.session.add(merchant1)
        db.session.commit()

        merchant2 = Merchant(username="testmerchant2", email="merchant@example.com", store_id=self.store.id)
        db.session.add(merchant2)
        
        with self.assertRaises(Exception):
            db.session.commit()

    def test_product_availability(self):
        product = Product(
            brand_name="Brand A",
            product_name="Product A",
            payment_status="Not Paid",
            received_items=100,
            closing_stock=100,
            buying_price=50.0,
            selling_price=70.0,
            store_id=self.store.id
        )
        db.session.add(product)
        db.session.commit()

        self.assertTrue(product.availability)

        product.closing_stock = 0
        db.session.commit()

        self.assertFalse(product.availability)

if __name__ == '__main__':
    unittest.main()
