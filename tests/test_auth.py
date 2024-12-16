import unittest
from app import create_app, db
from app.users.models import User, bcrypt


class UserTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app("test")
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        self.user = User(username="testuser", email="test@example.com")
        self.user.set_password("password123")
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_registration_login_page_loads(self):
        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_user_registration(self):
        response = self.client.post("/users/login/register", data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "confirm_password": "password123"
        })
        self.assertEqual(response.status_code, 302)

        user = User.query.filter_by(email="newuser@example.com").first()
        self.assertIsNotNone(user)
        self.assertTrue(bcrypt.check_password_hash(user.password, "password123"))

    def test_user_login(self):
        response = self.client.post("/users/login/login", data={
            "email": "test@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 302)

    def test_user_logout(self):
        self.client.post("/users/login/login", data={
            "email": "test@example.com",
            "password": "password123"
        })

        response = self.client.get("/users/logout")
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
