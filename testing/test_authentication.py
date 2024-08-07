
import unittest
from config import app, db
from models import Merchant, Admin, Clerk, Store, Product, SalesReport, Request
from unittest.mock import patch
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
     
     
     def test_login_success(self):
        with patch('app.User.query') as mock_query:
            mock_user = mock_query.filter_by.return_value.first.return_value
            mock_user.verify_password.return_value = True

            response = self.app.post(
                '/login',
                data=json.dumps({
                    "email": "testmerchant@example.com",
                    "role": "Merchant",
                    "password": "password123"
                }),
                content_type='application/json'
            )

            self.assertEqual(response.status_code, 201)
            self.assertIn('user', response.json)
            self.assertIn('access_token', response.json)

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

     def test_login_invalid_credentials(self, mock_query):
        mock_user = mock_query.filter_by.return_value.first.return_value
        mock_user.verify_password.return_value = False

        with app.test_request_context():
            response = self.app.post(
                '/login',
                data=json.dumps({
                    "email": "testmerchant@example.com",
                    "role": "Merchant",
                    "password": "wrongpassword"
                }),
                content_type='application/json'
            )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['error'], 'Unauthorized')

     def test_login_user_not_found(self):
        with patch('app.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = None

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



class TestGetSpecificStoreProducts(unittest.TestCase):
      def setUp(self):
        with app.app_context():
            store = Store(name="Test Store", location="Test Location")
            db.session.add(store)
            db.session.commit()

            product1 = Product(product_name="Product 1", store_id=store.id)
            product2 = Product(product_name="Product 2", store_id=store.id)
            db.session.add(product1)
            db.session.add(product2)
            db.session.commit()

      def test_get_specific_store_products(self):
        response = self.app.get('/getProducts/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

      def test_get_specific_store_products_invalid_store_id(self):
        response = self.app.get('/getProducts/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Store not found')



class TestSales(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            store = Store(name="Test Store", location="Test Location")
            db.session.add(store)
            db.session.commit()

            product = Product(product_name="Test Product", store_id=store.id, closing_stock=10, buying_price=5.0, selling_price=10.0)
            db.session.add(product)
            db.session.commit()

    def test_sale_recorded_successfully(self):
        response = self.app.post(
            '/sales/1',
            data=json.dumps({
                "date": "2022-01-01",
                "product_name": "Test Product",
                "quantity": 2,
                "total_price": 20.0
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)
        self.assertIn('product', response.json)
        self.assertIn('salesReport', response.json)

        product = Product.query.filter_by(product_name="Test Product").first()
        sales_report = SalesReport.query.filter_by(product_id=product.id).first()

        self.assertEqual(product.closing_stock, 8)
        self.assertEqual(sales_report.date, "2022-01-01")
        self.assertEqual(sales_report.quantity_sold, 2)
        self.assertEqual(sales_report.quantity_in_hand, 8)
        self.assertEqual(sales_report.profit, 10.0)

    def test_insufficient_stock(self):
        response = self.app.post(
            '/sales/1',
            data=json.dumps({
                "date": "2022-01-01",
                "product_name": "Test Product",
                "quantity": 20,
                "total_price": 200.0
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Insufficient stock')

    def test_product_not_found(self):
        response = self.app.post(
            '/sales/1',
            data=json.dumps({
                "date": "2022-01-01",
                "product_name": "Nonexistent Product",
                "quantity": 2,
                "total_price": 20.0
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Product not found')



class TestRequests(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            store = Store(name="Test Store", location="Test Location")
            db.session.add(store)
            db.session.commit()

            product = Product(product_name="Test Product", store_id=store.id)
            db.session.add(product)
            db.session.commit()

            clerk = Clerk(username="Test Clerk", email="testclerk@example.com", store_id=store.id)
            db.session.add(clerk)
            db.session.commit()

    def test_get_requests(self):
        response = self.app.get('/requests/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)

    def test_post_request(self):
        response = self.app.post(
            '/requests/1',
            data=json.dumps({
                "product_name": "Test Product",
                "stock": 10,
                "clerk_id": 1,
                "product_price": 5.0,
                "category": "Test Category"
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['quantity'], 10)
        self.assertEqual(response.json['product_id'], 1)
        self.assertEqual(response.json['clerk_id'], 1)
        self.assertEqual(response.json['store_id'], 1)

        request = Request.query.get(response.json['id'])
        self.assertIsNotNone(request)
        self.assertEqual(request.quantity, 10)
        self.assertEqual(request.product_id, 1)
        self.assertEqual(request.clerk_id, 1)
        self.assertEqual(request.store_id, 1)

    def test_post_request_product_not_found(self):
        response = self.app.post(
            '/requests/1',
            data=json.dumps({
                "product_name": "Nonexistent Product",
                "stock": 10,
                "clerk_id": 1,
                "product_price": 5.0,
                "category": "Test Category"
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'The product does not exist')




class TestPaymentStatus(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            product = Product(product_name="Test Product", payment_status="Unpaid")
            db.session.add(product)
            db.session.commit()

    def test_update_payment_status(self):
        response = self.app.get('/paymentStatus/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['payment_status'], 'Paid')

    def test_product_not_found(self):
        response = self.app.get('/paymentStatus/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Product not found')


class TestClerkAccountStatus(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            clerk = Clerk(username="Test Clerk", email="testclerk@example.com")
            db.session.add(clerk)
            db.session.commit()

    def test_change_account_status(self):
        response = self.app.get('/clerkAccountStatus/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Status changed to inactive')

    def test_delete_user(self):
        response = self.app.delete('/clerkAccountStatus/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User deleted successfully')

    def test_user_not_found(self):
        response = self.app.get('/clerkAccountStatus/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'User not found')



class TestAdminAccountStatus(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            admin = Admin(username="Test Admin", email="testadmin@example.com")
            admin.account_status = "active"
            db.session.add(admin)
            db.session.commit()

    def test_change_account_status(self):
        response = self.app.get('/adminAccountStatus/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Status changed to inactive')

        admin = Admin.query.filter_by(id=1).first()
        self.assertEqual(admin.account_status, 'inactive')

    def test_delete_admin(self):
        response = self.app.delete('/adminAccountStatus/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'User deleted successfully')

        admin = Admin.query.filter_by(id=1).first()
        self.assertIsNone(admin)



class TestAcceptRequests(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            store_id = 1
            request1 = Request(quantity=5, product_id=1, clerk_id=1, store_id=store_id)
            request2 = Request(quantity=3, product_id=2, clerk_id=2, store_id=store_id)
            db.session.add(request1)
            db.session.add(request2)
            db.session.commit()

    def test_accept_requests(self):
        response = self.app.get('/acceptRequests/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'All requests have been accepted and processed')

        requests = Request.query.filter_by(store_id=1).all()
        self.assertEqual(len(requests), 0)

        product1 = Product.query.get(1)
        product2 = Product.query.get(2)
        self.assertEqual(product1.closing_stock, 5)
        self.assertEqual(product2.closing_stock, 3)

    def test_accept_requests_no_requests(self):
        response = self.app.get('/acceptRequests/2')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'No requests found for this store')

    def test_delete_requests(self):
        response = self.app.delete('/acceptRequests/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Deleted 2 requests from the store')

        requests = Request.query.filter_by(store_id=1).all()
        self.assertEqual(len(requests), 0)

    def test_delete_requests_no_requests(self):
        response = self.app.delete('/acceptRequests/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Deleted 0 requests from the store')


if __name__ == '__main__':
    unittest.main()
