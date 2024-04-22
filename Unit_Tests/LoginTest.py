from django.test import TestCase
from ta_app.models import User
from classes.Login import Login


class LoginTests(TestCase):
    def setUp(self):
        User.objects.create(username='test@test.com', password='<PASSWORD>', fname='test', lname='test_lname', role='TA')

    def test_getUsername(self):
        user = Login(username='test@test.com', password='<PASSWORD>')
        self.assertEquals(user.getUsername('test'), 'test')

    def test_badUsername(self):
        user = Login(username='test1@test.com', password='<PASSWORD>')
        self.assertEquals(user.getUsername(), None, msg="Username not found")

    def test_getPassword(self):
        user = Login(username='test@test.com', password='<PASSWORD>')
        self.assertEquals(user.getPassword('<PASSWORD>'), '<PASSWORD>')

    def test_badPassword(self):
        user = Login(username='test@test.com', password='bad')
        self.assertEquals(user.getPassword('badPassword'), None, msg="Password not found")

    def test_getRole(self):
        user = Login(username='test@test.com', password='<PASSWORD>')
        self.assertEquals(user.getRole(), 'TA')

    def test_badRole(self):
        user = Login(username='test@test.com', password='<PASSWORD>')
        self.assertEquals(user.getRole(), None, msg="Role not found")

    def test_goodUser(self):
        user = Login(username='test@test.com', password='<PASSWORD>')
        self.assertEquals(user.findUser('test@test.com', '<PASSWORD>'), 'test@test.com')

    def test_badUser(self):
        user = Login(username='test1@test.com', password='<PASSWORD>')
        self.assertEquals(user.findUser('test1@test.com', '<PASSWORD>'), None, msg="User not found")