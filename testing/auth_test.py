import unittest

from app import app, db
from models import User
from flask_jwt_extended import create_access_token

app.secret_key = b'a\xdb\xd2\x13\x93\xc1\xe9\x97\xef2\xe3\x004U\xd1Z'

class TestApp(unittest.TestCase):
    '''Flask API in app.py'''

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()
            user = User(
                full_name='Test User',
                email='testuser@example.com',
                password='password'
            )
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_logs_user_in(self):
        '''logs user in by username and adds user_id to session at /login.'''
        with app.app_context():
            user = User.query.first()
            response = self.app.post('/login', json={
                'email': user.email,
                'password': 'password'
            })
            response_json = response.get_json()

            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response_json['user']['id'], user.id)
            self.assertEqual(response_json['user']['full_name'], user.full_name)
            self.assertIn('access_token', response_json)

    def test_logs_user_out(self):
        '''removes user_id from session at /logout.'''
        with app.app_context():
            user = User.query.first()
            access_token = create_access_token(identity=user)

            response = self.app.delete('/logout', headers={
                'Authorization': f'Bearer {access_token}'
            })

            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.data, b'')

    def test_checks_session(self):
        '''checks session for user_id at /check_session.'''
        with app.app_context():
            user = User.query.first()
            access_token = create_access_token(identity=user)

            logged_in_response = self.app.get('/check_session', headers={
                'Authorization': f'Bearer {access_token}'
            })
            logged_in_json = logged_in_response.get_json()

            self.assertEqual(logged_in_response.content_type, 'application/json')
            self.assertEqual(logged_in_response.status_code, 200)
            self.assertEqual(logged_in_json['user']['id'], user.id)
            self.assertEqual(logged_in_json['user']['full_name'], user.full_name)

            # Simulate logging out
            self.app.delete('/logout', headers={
                'Authorization': f'Bearer {access_token}'
            })

            logged_out_response = self.app.get('/check_session', headers={
                'Authorization': f'Bearer {access_token}'
            })
            logged_out_json = logged_out_response.get_json()

            self.assertEqual(logged_out_response.status_code, 401)
            self.assertEqual(logged_out_json, {})

if __name__ == '__main__':
    unittest.main()
