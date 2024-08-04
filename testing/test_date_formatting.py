import unittest
from app import create_app
from app.utils import format_date

class DateFormattingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_date_formatting(self):
        raw_date = '2024-08-04T15:26:35.000Z'
        formatted_date = format_date(raw_date)
        self.assertEqual(formatted_date, 'August 4, 2024 15:26')
