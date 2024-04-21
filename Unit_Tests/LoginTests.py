import unittest
from ta_app.models import User
from classes import Login


class LoginTests(unittest.TestCase):
    def setUp(self):
        User.objects.create(username='test', password='<PASSWORD>', fname='test', lname='test_lname', role='TA')

    def test_getUsername(self):
        self.assertEquals(Login.getUsername('test'), 'test')

    def test_badUsername(self):
        username = Login.getUsername('badUser')
        self.assertEquals(username, None, msg="Username not found")

    def test_getPassword(self):
        self.assertEquals(Login.getPassword('<PASSWORD>'), '<PASSWORD>')

    def test_badPassword(self):
        self.assertEquals(Login.getPassword('badPassword'), '<PASSWORD>', msg="Password not found")

    def test_getRole(self):
        self.assertEquals(Login.getRole('TA'), 'TA')

    def test_badRole(self):
        self.assertEquals(Login.getRole('badRole'), None, msg="Role not found")



