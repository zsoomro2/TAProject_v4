from datetime import datetime
from django.test import TestCase, Client
from ta_app.models import User, Course


# Create your tests here.

class Login(TestCase):
    client = None

    def setUp(self):
        self.client = Client()
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='TA')

        test_user2 = User.objects.create(username='test2@test.com', password='test2', fname='test_name2',
                                         lname='test_lname2', role="Instructor")

        test_user3 = User.objects.create(username='test3@test', password='test3', fname='test_name3',
                                         lname='test_lname3', role="Supervisor")

    def test_userSupervisor(self):
        resp = self.client.post('', {'username': 'test3@test.com', 'password': 'test3'})
        self.assertEqual(resp.status_code, 200)

    def test_userInstructor(self):
        resp = self.client.post('', {'username': 'test2@test.com', 'password': 'test2'})
        self.assertEqual(resp.status_code, 200)

    def test_userTA(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'})
        self.assertEqual(resp.status_code, 200)

    def test_badUsername(self):
        resp = self.client.post('', {'username': 'badUser@test.com', 'password': '<PASSWORD>'}, follow=True)
        self.assertEqual(resp.context["message"], "There was an error logging you in, please try again")

    def test_badPassword(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': '<PA>'}, follow=True)
        self.assertEqual(resp.context["message"], "There was an error logging you in, please try again")


class AddUserTestCase(TestCase):
    client = Client()
    def setUp(self):
        self.client = Client()
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='TA')

    def test_badUser(self):
        resp = self.client.post('/adduser/', {'username': 'test', 'password': 'test3', 'fname': 'test_name3',
                                              'lname': 'test_lname3', 'role': 'Supervisor'})
        user = User.objects.filter(username="test")
        self.assertEqual(resp.context['message'], "There was an error validating the form")

    def test_badData(self):
        resp = self.client.post('/adduser/', {'username': 'test1@test.com', 'password': 'test3', 'fname': '',
                                              'lname': 'test_lname3', 'role': 'Supervisor'})
        self.assertEqual(resp.context['message'], "There was an error validating the form")

    def test_addExistingUser(self):
        resp = self.client.post('/adduser/', {'username': 'test@test.com', 'password': 'test3', 'fname': 'test_name3',
                                              'lname': 'test_lname3', 'role': 'Supervisor'})
        self.assertEqual(resp.context['message'], "User already exists")

    def test_addUser(self):
        resp = self.client.post('/adduser/', {'username': 'test3@test.com', 'password': '<PASSWORD>',
                                              'fname': 'test_name', 'lname': 'test_lname', 'role': 'TA'})
        self.assertEqual(resp.context['message'], "You have successfully added test3@test.com")

    def test_addBadRole(self):
        resp = self.client.post('/adduser/', {'username': 'test3@test.com', 'password': '<PASSWORD>',
                                              'fname': 'test_name', 'lname': 'test_lname', 'role': 'Role'})
        self.assertEqual(resp.context['message'], "There was an error validating the form")

class LogoutTest(TestCase):
    client = None
