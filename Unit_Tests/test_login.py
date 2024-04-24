from django.test import TestCase
from ta_app.models import User
from classes.Login import Login

class LoginTests(TestCase):
    def setUp(self):
        User.objects.create(username='test@test.com', password='<PASSWORD>', fname='test', lname='test_lname', role='TA')
    def test_getUsername(self):
        user = Login(username='test@test.com', password='<PASSWORD>')
        self.assertEqual(user.getUsername(), 'test@test.com')
    def test_getPassword(self):
        user = Login(username='test@test.com', password='<PASSWORD>')
        self.assertEqual(user.getPassword(), '<PASSWORD>')
    def test_getRole(self):
        user = Login(username='test@test.com', password='<PASSWORD>')
        self.assertEqual(user.getRole(), 'TA')
    def test_badRole(self):
        user = Login(username='test1@test.com', password='<PASSWORD>')
        self.assertEqual(user.getRole(), None, msg="Role not found")
    def test_goodUser(self):
        user = Login(username='test@test.com', password='<PASSWORD>')
        self.assertEqual(user.findUser('test@test.com', '<PASSWORD>').username, 'test@test.com')
    def test_badUser(self):
        user = Login(username='test1@test.com', password='<PASSWORD>')
        self.assertEqual(user.findUser('test1@test.com', '<PASSWORD>'), None, msg="User not found")