import unittest
from app import create_app, db
from models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.superuser = User(email='superuser@example.com', password='superpassword', role='superuser')
            db.session.add(self.superuser)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_superuser_can_initiate_registration(self):
        response = self.client.post('/register', json={'email': 'admin@example.com'}, headers={'Authorization': f'Bearer {self.superuser_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Registration link sent.', response.get_data(as_text=True))

    def test_admin_registration_with_valid_token(self):
        # Assuming a registration token is generated and stored
        registration_token = 'valid_token'
        response = self.client.post('/register/confirm', json={'token': registration_token, 'password': 'newpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Registration successful.', response.get_data(as_text=True))

    def test_login_with_valid_credentials(self):
        response = self.client.post('/login', json={'email': 'admin@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())
