import unittest
from test_config import app, db
from test_model import Merchant,Admin, Store, Product, SalesReport, Request
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



    def test_invite_admin_already_exists(self):
        with app.app_context():
      
            existing_admin = Admin(email="existingadmin@example.com", role="Admin", account_status="active", store_id=1)
            db.session.add(existing_admin)
            db.session.commit()

            response = self.app.post(
                '/inviteAdmin',
                data=json.dumps({
                    "email": "existingadmin@example.com",
                    "store_id": 1
                }),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json['error'], 'Unauthorized')

    def test_signup_email_exists(self):
        with app.app_context():
            
            store = Store(name="Test Store", location="Test Location")
            db.session.add(store)
            db.session.commit()

            admin = Admin(username="Test Admin", email="existingadmin@example.com", store_id=store.id)
            admin.password_hash = "password123"
            db.session.add(admin)
            db.session.commit()

            
            response = self.app.post(
                '/inviteAdmin',
                data=json.dumps({
                    "full_name": "Test Admin",
                    "email": "existingadmin@example.com",
                    "role": "Admin",
                    "store_id": store.id,
                    "password": "password123"
                }),
                content_type='application/json'
            )

            
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json['error'], 'Unauthorized')

    def test_invite_admin_missing_email(self):
        response = self.app.post(
            '/inviteAdmin',
            data=json.dumps({
                "store_id": 1
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
     

    def test_invite_admin_missing_store_id(self):
        response = self.app.post(
            '/inviteAdmin',
            data=json.dumps({
                "email": "newadmin@example.com"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
       


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