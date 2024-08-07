import unittest
from flask import json
from config import app, db
from models import Merchant, Admin, Clerk, Store

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Create all tables
        with app.app_context():
            db.create_all()

        # Create test data
        self.create_test_data()

    def tearDown(self):
        # Drop all tables
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def create_test_data(self):
        # Create a test store
        store = Store(name="Test Store", location="Test Location")
        db.session.add(store)
        db.session.commit()

        # Create test users
        self.test_merchant = Merchant(username="merchant1", email="merchant1@test.com", store_id=store.id)
        self.test_merchant.password_hash = "password123"
        db.session.add(self.test_merchant)

        self.test_admin = Admin(username="admin1", email="admin1@test.com", store_id=store.id)
        self.test_admin.password_hash = "password123"
        db.session.add(self.test_admin)

        self.test_clerk = Clerk(username="clerk1", email="clerk1@test.com", store_id=store.id)
        self.test_clerk.password_hash = "password123"
        db.session.add(self.test_clerk)

        db.session.commit()

    def get_access_token(self, email, password, role):
        response = self.app.post('/login', data=json.dumps({
            'email': email,
            'password': password,
            'role': role
        }), content_type='application/json')
        return json.loads(response.data)['access_token']

class TestAuthEndpoints(BaseTestCase):
    def test_signup(self):
        response = self.app.post('/signup', data=json.dumps({
            'full_name': 'new_merchant',
            'email': 'new_merchant@test.com',
            'role': 'Merchant',
            'store_id': 1,
            'password': 'password123',
            'phone_number': '1234567890'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('access_token', json.loads(response.data))

    def test_login(self):
        response = self.app.post('/login', data=json.dumps({
            'email': 'merchant1@test.com',
            'password': 'password123',
            'role': 'Merchant'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('access_token', json.loads(response.data))

    def test_check_session(self):
        access_token = self.get_access_token('merchant1@test.com', 'password123', 'Merchant')
        response = self.app.get('/check_session', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)

class TestStoreEndpoints(BaseTestCase):
    def test_get_products(self):
        access_token = self.get_access_token('merchant1@test.com', 'password123', 'Merchant')
        response = self.app.get('/getProducts/1', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)

class TestSalesEndpoints(BaseTestCase):
    def test_get_sales(self):
        access_token = self.get_access_token('merchant1@test.com', 'password123', 'Merchant')
        response = self.app.get('/sales/1', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)

    def test_post_sales(self):
        access_token = self.get_access_token('merchant1@test.com', 'password123', 'Merchant')
        response = self.app.post('/sales/1', data=json.dumps({
            'date': '2024-08-07',
            'product_name': 'Test Product',
            'quantity': 10,
            'total_price': 100.0
        }), headers={'Authorization': f'Bearer {access_token}'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
