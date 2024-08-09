import unittest
from config import app, db
from models import Merchant, Store, Product, SalesReport, Request
from unittest.mock import patch, MagicMock
from flask import json

class TestSignUp(unittest.TestCase):

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

    def test_signup_success(self):
        with app.app_context():
            store = Store(name="Test Store", location="Test Location")
            db.session.add(store)
            db.session.commit()

            response = self.app.post(
                '/signup',
                data=json.dumps({
                    "full_name": "Test Merchant",
                    "email": "testmerchant@example.com",
                    "role": "Merchant",
                    "store_id": store.id,
                    "password": "password123"
                }),
                content_type='application/json'
            )

            self.assertEqual(response.status_code, 201)
            self.assertIn('user', response.json)
            self.assertIn('access_token', response.json)

            retrieved_merchant = Merchant.query.filter_by(email="testmerchant@example.com").first()
            self.assertIsNotNone(retrieved_merchant)
            self.assertTrue(retrieved_merchant.verify_password("password123"))

    def test_signup_invalid_role(self):
        response = self.app.post(
            '/signup',
            data=json.dumps({
                "full_name": "Test User",
                "email": "testuser@example.com",
                "role": "InvalidRole",
                "store_id": 1,
                "password": "password123"
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Invalid role')

    def test_signup_email_exists(self):
        with app.app_context():
            store = Store(name="Test Store", location="Test Location")
            db.session.add(store)
            db.session.commit()

            merchant = Merchant(username="Test Merchant", email="existingmerchant@example.com", store_id=store.id)
            merchant.password_hash = "password123"
            db.session.add(merchant)
            db.session.commit()

            response = self.app.post(
                '/signup',
                data=json.dumps({
                    "full_name": "Test Merchant",
                    "email": "existingmerchant@example.com",
                    "role": "Merchant",
                    "store_id": store.id,
                    "password": "password123"
                }),
                content_type='application/json'
            )

            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json['error'], 'Email already registered, kindly log in')

    def test_signup_missing_fields_5(self):
        response = self.app.post(
            '/signup',
            data=json.dumps({
                "full_name": "Test Merchant",
                "email": "testmerchant@example.com",
                "role": "Merchant",
                "store_id": 1
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 422)
        self.assertIn('error', response.json)


class TestLogin(unittest.TestCase):

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

   
    def test_login_invalid_role(self):
        response = self.app.post(
            '/login',
            data=json.dumps({
                "email": "testuser@example.com",
                "role": "InvalidRole",
                "password": "password123"
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], 'Invalid role')

   

    def test_login_user_not_found(self):
        with app.app_context():
            with patch('models.Merchant.query.filter_by') as mock_query:
                mock_query.return_value.first.return_value = None

                response = self.app.post(
                    '/login',
                    data=json.dumps({
                        "email": "nonexistent@example.com",
                        "role": "Merchant",
                        "password": "password123"
                    }),
                    content_type='application/json'
                )

                self.assertEqual(response.status_code, 401)
                self.assertEqual(response.json['error'], 'Unauthorized')


class TestSales(unittest.TestCase):


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

    def setUp(self):
        with app.app_context():
            store = Store(name="Test Store", location="Test Location")
            db.session.add(store)
            db.session.commit()

            product = Product(product_name="Test Product", store_id=store.id, closing_stock=10, buying_price=5.0, selling_price=10.0, brand_name="Test Brand")
            db.session.add(product)
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
