from django.test import TestCase
from ta_app.models import User
from classes.AddUser import AddUser


class AddUserTests(TestCase):
    def setUp(self):
        User.objects.create(username='test@test.com', password='<PASSWORD>', fname='test', lname='test_lname', role='TA')

    def test_validate(self):
        user1 = AddUser(username='test@test.com', password='<PASSWORD>', fname='test_name', lname='test_lname', role='TA')
        user2 = AddUser(username='test1@test.com', password='<PASSWORD>', fname="", lname='test_lname', role='TA')
        user3 = AddUser(username='test1test.com', password='<PASSWORD>', fname='test_name', lname='test_lname', role='TA')

        self.assertEqual(user1.validate(), True)
        self.assertEqual(user2.validate(), False)
        self.assertEqual(user3.validate(), False)

    def test_checkUser(self):
        user1 = AddUser(username='test@test.com', password='<PASSWORD>', fname='test', lname='test_lname', role='TA')
        user2 = AddUser(username='test1@test.com', password='<PASSWORD>', fname=None, lname='test_lname', role='TA')
        self.assertEqual(user1.checkUser(), True)
        self.assertEqual(user2.checkUser(), False)