import unittest
from ta_app.models import User
from classes import Login


class LoginTests(unittest.TestCase):
    def setUp(self):
        User.objects.create_user(username='test', password='<PASSWORD>')

    def test_getUsername(self):
        self.assertEquals(User.objects.getUsername('test'), 'test')

    def test_badUsername(self):
        try:
            username = User.objects.getUsername('')
        except Exception as e:
            with self.assertRaises(e, msg="User not found"):
                username = User.objects.getUsername('')

