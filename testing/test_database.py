import unittest
from app import create_app, db
from models import Product, Store, Clerk

class DatabaseNormalizationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_database_relationships(self):
        store = Store(name='Main Store')
        product = Product(name='Product 1', price=10.0)
        clerk = Clerk(name='Clerk 1', store=store)
        db.session.add(store)
        db.session.add(product)
        db.session.add(clerk)
        db.session.commit()

        self.assertEqual(len(store.clerks), 1)
        self.assertEqual(clerk.store.name, 'Main Store')
