from datetime import datetime
from django.test import TestCase, Client
from ta_app.models import User, Course, Section, LecLab, MeetType
from datetime import datetime, timezone

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
        resp = self.client.post('', {'username': 'test3@test.com', 'password': 'test3'}, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_userInstructor(self):
        resp = self.client.post('', {'username': 'test2@test.com', 'password': 'test2'}, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_userTA(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_badUsername(self):
        resp = self.client.post('', {'username': 'badUser@test.com', 'password': '<PASSWORD>'}, follow=True)
        self.assertEqual(resp.context["message"], "Login failed. Please try again.")

    def test_badPassword(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': '<PA>'}, follow=True)
        self.assertEqual(resp.context["message"], "Login failed. Please try again.")


class AddUserTestCase(TestCase):
    client = Client()
    def setUp(self):
        self.client = Client()
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

    def test_badUser(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='test@test.com', password='test')

        resp = self.client.post('/adduser/', {'username': 'test', 'password': 'test3', 'fname': 'test_name3',
                                              'lname': 'test_lname3', 'role': 'Supervisor'}, follow=True)

        self.assertEqual(resp.context['message'], "There was an error validating the form")

    def test_badData(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='test@test.com', password='test')

        resp = self.client.post('/adduser/', {'username': 'test1@test.com', 'password': 'test3', 'fname': '',
                                              'lname': 'test_lname3', 'role': 'Supervisor'})
        self.assertEqual(resp.context['message'], "There was an error validating the form")

    def test_addExistingUser(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='test@test.com', password='test')

        resp = self.client.post('/adduser/', {'username': 'test@test.com', 'password': 'test3', 'fname': 'test_name3',
                                              'lname': 'test_lname3', 'role': 'Supervisor'})
        self.assertEqual(resp.context['message'], "User already exists")

    def test_addUser(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='test@test.com', password='test')

        resp = self.client.post('/adduser/', {'username': 'test3@test.com', 'password': '<PASSWORD>',
                                              'fname': 'test_name', 'lname': 'test_lname', 'role': 'TA'})
        self.assertEqual(resp.context['message'], "You have successfully added test3@test.com")

    def test_addBadRole(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='test@test.com', password='test')

        resp = self.client.post('/adduser/', {'username': 'test3@test.com', 'password': '<PASSWORD>',
                                              'fname': 'test_name', 'lname': 'test_lname', 'role': 'Role'})
        self.assertEqual(resp.context['message'], "There was an error validating the form")

    def test_addBadUsername(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='test@test.com', password='test')

        resp = self.client.post('/adduser/', {'username': 'test', 'password': '<PASSWORD>',
                                              'fname': 'test_name', 'lname': 'test_lname', 'role': 'TA'})
        self.assertEqual(resp.context['message'], "There was an error validating the form")

class EditTestCase(TestCase):
    client = Client()
    def setUp(self):
        self.client = Client()

    def test_editUser(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/edit.html/test@test.com', {'username':'test@test.com', 'fname':'test_name',
                                                            'lname':'test_lname', 'role':'Supervisor'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/edit.html/test@test.com', {'username':'test1@test.com', 'fname':'test_name',
                                                             'lname':'test_lname', 'role':'Supervisor'}, follow=True)
        updated_user = User.objects.get(username='test1@test.com')
        self.assertEqual(updated_user.username, 'test1@test.com')

    def test_badUsernameEdit(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')
        test_user = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/edit.html/test@test.com', {'username':'test@test.com', 'password':'test',
                                'fname':'test_name', 'lname':'test_lname', 'role':'Supervisor'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/edit.html/test@test.com', {'username':'test1@test.com', 'password':'test',
                                'fname':'test_name', 'lname':'test_lname', 'role':'Supervisor'}, follow=True)
        self.assertEqual(resp.context['message'], "Error when updating user")

    def test_badEmail(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')
        test_user = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='test@test.com', password='test')

        resp = self.client.get('/edit.html/test@test.com', {'username':'test@test.com', 'password':'test',
                                'fname':'test_name', 'lname':'test_lname', 'role':'Supervisor'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/edit.html/test@test.com', {'username':'testtest.com', 'password':'test',
                                'fname':'test_name', 'lname':'test_lname', 'role':'Supervisor'}, follow=True)

        with self.assertRaises(User.DoesNotExist, msg="User does not exist"):
            user = User.objects.get(username='testtest.com')
        updated_user = User.objects.get(username="test@test.com")
        self.assertEqual(updated_user.username, 'test@test.com')

    def test_userEditOtherUser(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='TA')
        test_user2 = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Instructor')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='test@test.com', password='test')

        resp = self.client.get('/edit.html/test1@test.com', {'username': 'test1@test', 'password': 'test',
                                'fname':'test_name', 'lname': 'test_lname', 'role': 'Supervisor'})
        self.assertEqual(resp.status_code, 302)

    def test_userEditOwnProfile(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='TA')

        resp = self.client.post('', {'username':'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='test@test.com', password='test')

        resp = self.client.get('/edit.html/test@test.com', {'username': 'test@test.com', 'fname':'test_name',
                                                            'lname': 'test_lname'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post('/edit.html/test@test.com', {'username': 'test1@test.com', 'fname':'test_name',
                                                             'lname': 'test_lname'}, follow=True)
        updated_user = User.objects.get(username='test1@test.com')
        self.assertEqual(updated_user.username, 'test1@test.com')
    def test_editCourse(self):
        test_course = Course.objects.create(Course_name="Math 101", Course_description="abc", MeetType="Online")
        test_user = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username':'test1@test.com', 'password':'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.client.login(username='test1@test.com', password='test')
        resp = self.client.get('/edit.html/Math%20101', {'CourseName':'Math 101', 'MeetType':'Online',
                                                         'course_desc':'abc'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Math 101")

        resp = self.client.post('/edit.html/Math%20101', {'CourseName':'Math 102', 'MeetType':'Online',
                                                                    'course_desc':'abc'}, follow=True)

        course = Course.objects.get(Course_name='Math 102')
        self.assertEqual(course.Course_name, 'Math 102')

    def test_editBadCourseName(self):
        test_course = Course.objects.create(Course_name="Math 101", Course_description="", MeetType="Online")
        test_course = Course.objects.create(Course_name="Math 100", Course_description="", MeetType="Online")
        test_user = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username':'test1@test.com', 'password':'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.client.login(username='test1@test.com', password='test')
        resp = self.client.get('/edit.html/Math%20101', {'CourseName':'Math 101', 'course_desc':'',
                                                         'MeetType':'Online'})
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post('/edit.html/Math%20101', {'CourseName':'Math 100', 'course_desc':'',
                                                          'MeetType':'Online'})
        self.assertEqual(resp.context['message'], "There was an error updating the course")

    def test_badUserTryToEdit(self):
        test_course = Course.objects.create(Course_name="Math 100", Course_description="", MeetType="Online")
        test_user = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='TA')
        resp = self.client.post('', {'username':'test1@test.com', 'password':'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.client.login(username='test1@test.com', password='test')
        resp = self.client.get('/edit.html/Math%20100', {'CourseName':'Math 100', 'course_desc':'',
                                                         'MeetType':'Online'})
        self.assertEqual(resp.status_code, 302)
class test_addCourse(TestCase):
    def setUp(self):
        self.client = Client()
        test_course = Course.objects.create(Course_name="Math 101", Course_description="", MeetType="Online")

    def test_addCourse(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username':'test@test.com', 'password':'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='test@test.com', password='test')

        resp = self.client.get('/addcourse/', follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/addcourse/', {'CourseName':'Math 100', 'coursedesc':'',
                                                'MeetType':'Online'})
        self.assertEqual(resp.context['message'], "You have successfully added Math 100")

    def test_badCourseName(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username':'test@test.com', 'password':'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='test@test.com', password='test')

        resp = self.client.post('/addcourse/', {'CourseName':'Math 101', 'coursedesc':'', 'MeetType':'Online'})
        self.assertEqual(resp.context['message'], "Course already exists")

    def test_badUserTriesToAddCourse(self):
        test_user = User.objects.create(username='test2@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='TA')

        resp = self.client.post('', {'username':'test2@test.com', 'password':'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username='test2@test.com', password='test')

        resp = self.client.get('/addcourse/', {})
        self.assertEqual(resp.status_code, 302)
class test_addSection(TestCase):
    def setUp(self):
        self.client = Client()
        start = datetime.strptime("2022-01-01 12:00:00", "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime("2023-01-01 12:00:00", "%Y-%m-%d %H:%M:%S")
        test_course = Course.objects.create(Course_name="Math 101", Course_description="", MeetType="Online")
        course = Course.objects.get(Course_name="Math 101")
        test_section = Section.objects.create(Course=course, section_number="401", LecLab="Lecture", start=start,
                                              end=end, credits=4, instructor=None, ta=None)

    def test_addSection(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username':'test@test.com', 'password':'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.client.login(username="test@test.com", password="test")

        resp = self.client.get('/addsection/Math%20101', {'course_name':'Math 101'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        course = Course.objects.get(Course_name="Math 101")
        start = datetime.strptime("2022-01-01T12:00", "%Y-%m-%dT%H:%M").replace(tzinfo=None)
        end = datetime.strptime("2023-02-02T12:00", "%Y-%m-%dT%H:%M").replace(tzinfo=None)

        resp = self.client.post('/addsection/Math%20101', {'course_name':course, 'sec_num': '402',
                                    'LecLab':'Lecture', 'start':start, 'end':end, 'credits':'4',
                                    'instructor':'None', 'ta':'None'}, follow=True)

        self.assertEqual(resp.conext['message'], "You have added 402 to Math 101")
class LogoutTest(TestCase):
    client = None

