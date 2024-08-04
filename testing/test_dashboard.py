import unittest
from app import create_app

class DashboardTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_custom_dashboard_access(self):
        # Test access for different user roles
        response = self.client.get('/dashboard', headers={'Authorization': 'Bearer clerk_token'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Dashboard Data', response.get_data(as_text=True))
