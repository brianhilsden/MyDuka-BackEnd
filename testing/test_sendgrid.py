import unittest
from app import create_app
from app.utils import send_email

class SendGridTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_send_email(self):
        response = send_email('test@example.com', 'Test Subject', 'Test Body')
        self.assertTrue(response)
