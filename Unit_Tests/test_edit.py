from django.test import TestCase
from ta_app.models import User, Course, Roles
from classes.AddUser import AddUser
from classes.EditClass import EditClass


class LoginTests(TestCase):
    def setUp(self):
        User.objects.create(username='test@test.com', password='<PASSWORD>', fname='test', lname='test_lname', role='TA')

    def test_goodUser(self):
        user = AddUser(username="test@test.com", password="<PASSWORD>", fname="test", lname="test_lname", role="Instructor")
