from django.test import TestCase
from classes.User import User


class TestUser(TestCase):

    def setUp(self):
        self.user = User("john_doe", "securepassword123", "John", "Doe", "1234567890", "admin")

    def test_get_username(self):
        self.assertEqual(self.user.get_username(), "john_doe")

    def test_get_password(self):
        self.assertEqual(self.user.get_password(), "securepassword123")

    def test_get_firstName(self):
        self.assertEqual(self.user.get_firstName(), "John")

    def test_get_lastName(self):
        self.assertEqual(self.user.get_lastName(), "Doe")

    def test_get_phone(self):
        self.assertEqual(self.user.get_phone(), "1234567890")

    def test_get_role(self):
        self.assertEqual(self.user.get_role(), "admin")
