import unittest
from app import create_app
from app.utils import paginate

class PaginationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_paginate(self):
        data = list(range(100))
        page = 2
        per_page = 10
        paginated_data = paginate(data, page, per_page)
        self.assertEqual(len(paginated_data), per_page)
        self.assertEqual(paginated_data[0], 10)
