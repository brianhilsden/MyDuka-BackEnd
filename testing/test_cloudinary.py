import unittest
from app import create_app
from app.utils import upload_image

class CloudinaryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_image_upload_and_resize(self):
        with open('test_image.jpg', 'rb') as image:
            response = upload_image(image)
            self.assertIn('url', response)
            self.assertTrue(response['width'] <= 800)
