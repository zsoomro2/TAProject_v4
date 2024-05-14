from django.test import TestCase
from ta_app.models import User
from classes.AddUser import AddUser


class AddUserTests(TestCase):
    def setUp(self):
        User.objects.create(username='test@test.com', password='<PASSWORD>', fname='test', lname='test_lname',
                            role='TA')

    def test_validate(self):
        user = AddUser(username='test@test.com', password='<PASSWORD>', fname='test_name', lname='test_lname',
                        role='TA')
        self.assertEqual(user.validate(), True)

    def test_emptyFName(self):
        user = AddUser(username='test1@test.com', password='<PASSWORD>', fname="", lname='test_lname', role='TA')
        self.assertEqual(user.validate(), False)

    def test_emptyLName(self):
        user = AddUser(username='test1@test.com', password='<PASSWORD>', fname='test_name', lname="", role='TA')
        self.assertEqual(user.validate(), False)

    def test_emptyUser(self):
        user = AddUser(username="", password="<PASSWORD>", fname="test_name", lname="test_lname", role="TA")
        self.assertEqual(user.validate(), False)

    def test_emptyPassword(self):
        user = AddUser(username='test1@test.com', password='', fname='test_name', lname='test_lname', role='TA')
        self.assertEqual(user.validate(), False)

    def test_badUsername(self):
        user = AddUser(username='test1test.com', password='<PASSWORD>', fname='test_name', lname='test_lname',
                        role='TA')
        self.assertEqual(user.validate(), False)

    def test_badRole(self):
        user = AddUser(username='test1@test.com', password='<PASSWORD>', fname=None, lname='test_lname', role='Role')
        self.assertEqual(user.validate(), False)

    def test_checkUser(self):
        user = AddUser(username='test@test.com', password='<PASSWORD>', fname='test', lname='test_lname', role='TA')
        self.assertEqual(user.checkUser(), True)

    def test_checkBadInfo(self):
        user = AddUser(username='test1@test.com', password='<PASSWORD>', fname=None, lname='test_lname', role='TA')
        self.assertEqual(user.checkUser(), False)




