import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_greetings_page(self):
        """Тест маршруту /hi/<name>."""
        response = self.client.get("/users/hi/Jonathan?age=30")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Jonathan", response.data)
        self.assertIn(b"30", response.data)

    def test_admin_page(self):
        """Тест маршруту /admin, який перенаправляє."""
        response = self.client.get("/users/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Administrator", response.data)
        self.assertIn(b"20", response.data)

if __name__ == "__main__":
#    unittest = unittest.TestLoader().loadTestsFromTestCase(FlaskAppTestCase)
    unittest.main()