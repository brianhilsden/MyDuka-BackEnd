import unittest
from app import create_app
from app.forms import ProductForm

class ValidationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_product_form_validation(self):
        form = ProductForm(data={'name': '', 'price': -10})
        self.assertFalse(form.validate())
        self.assertIn('Name is required', form.errors['name'])
        self.assertIn('Price must be greater than zero', form.errors['price'])
