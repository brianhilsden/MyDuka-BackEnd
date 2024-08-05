import unittest
from config import app, db, bcrypt
from models import Merchant, Admin, Clerk, Store
from flask import Flask

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

if __name__ == '__main__':
    unittest.main()
