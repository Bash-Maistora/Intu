import unittest
from app import app


class CategoryTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_status_code(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_API_home(self):
        result = self.app.get('/')
        self.assertEqual(result.data, b'Submit a category as query parameter.')

    def test_API_normalizing(self):
        result_caps = self.app.get('/?category="MEN FOOTWEAR."')
        result_dash = self.app.get('/?category="men - new- bags.')
        result_chars = self.app.get('/?category="women=$ accessories _ new"')
        result_numbers = self.app.get('/?category="23male5shoes4"')

        self.assertEqual(result_caps.data, b'/Men/Footwear')
        self.assertEqual(result_dash.data, b'/Men/Bags')
        self.assertEqual(result_chars.data, b'/Women/Accessories')
        self.assertEqual(result_numbers.data, b'/Men/Footwear')

    def test_API_categorizing(self):
        result_one_cat = self.app.get('/?category="male Footwear"')
        result_two_cat = self.app.get('/?category="females skirt"')
        result_info = self.app.get('/?category="man shirt new model"')
        result_info_chars = self.app.get('/?category="spring - collection - womens - jewelry."')

        self.assertEqual(result_one_cat.data, b'/Men/Footwear')
        self.assertEqual(result_two_cat.data, b'/Women/Dresses')
        self.assertEqual(result_info.data, b'/Men/Clothing')
        self.assertEqual(result_info_chars.data, b'/Women/Jewellery')

    def test_equal(self):
        self.assertEqual(2, 2)

if __name__ == '__main__':
    unittest.main()
