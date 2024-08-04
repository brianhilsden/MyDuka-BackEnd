import unittest
from app import create_app

class ErrorHandlingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_404_error(self):
        response = self.client.get('/nonexistent_endpoint')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Not Found', response.get_data(as_text=True))
