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

        resp = self.client.post('/adduser/', {'username': 'test', 'password': 'test3', 'fname': 'test_name3',
                                              'lname': 'test_lname3', 'role': 'Supervisor'}, follow=True)

        self.assertEqual(resp.context['message'], "There was an error validating the form")

    def test_badData(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/adduser/', {'username': 'test1@test.com', 'password': 'test3', 'fname': '',
                                              'lname': 'test_lname3', 'role': 'Supervisor'})
        self.assertEqual(resp.context['message'], "There was an error validating the form")

    def test_addExistingUser(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/adduser/', {'username': 'test@test.com', 'password': 'test3', 'fname': 'test_name3',
                                              'lname': 'test_lname3', 'role': 'Supervisor'})
        self.assertEqual(resp.context['message'], "User already exists")

    def test_addUser(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/adduser/', {'username': 'test3@test.com', 'password': '<PASSWORD>',
                                              'fname': 'test_name', 'lname': 'test_lname', 'role': 'TA'})
        self.assertEqual(resp.context['message'], "You have successfully added test3@test.com")

        user = User.objects.get(username='test3@test.com')
        self.assertEqual(user.username, 'test3@test.com')

    def test_addBadRole(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/adduser/', {'username': 'test3@test.com', 'password': '<PASSWORD>',
                                              'fname': 'test_name', 'lname': 'test_lname', 'role': 'Role'})
        self.assertEqual(resp.context['message'], "There was an error validating the form")

    def test_addBadUsername(self):
        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/adduser/', {'username': 'test', 'password': '<PASSWORD>',
                                              'fname': 'test_name', 'lname': 'test_lname', 'role': 'TA'})
        self.assertEqual(resp.context['message'], "There was an error validating the form")


class EditUserTestCase(TestCase):
    client = Client()

    def setUp(self):
        self.client = Client()
    def test_editUser(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')
        self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)

        resp = self.client.post('/edit.html/test@test.com', {'fname': 'test_name', 'lname': 'test_lname',
                                                             'username': 'test@test.com',
                                                             'role': 'TA'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        updated_user = User.objects.get(username='test@test.com')
        self.assertEqual(updated_user.role, 'TA')

    def test_editUserNoFName(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')
        self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)

        resp = self.client.post('/edit.html/test@test.com', {'fname': '', 'lname': 'test_lname',
                                                             'username': 'test@test.com', 'password': '<PASSWORD>',
                                                             'role': 'TA'}, follow=True)
        self._assert_contains(response=resp, text="Please fill out this field.", status_code=200, msg_prefix='',
                              html=False)

    def test_editUserNoLName(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')
        self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)

        resp = self.client.post('/edit.html/test@test.com', {'fname': 'test_name', 'lname': '',
                                                             'username': 'test@test.com', 'password': '<PASSWORD>',
                                                             'role': 'TA'}, follow=True)
        self._assert_contains(response=resp, text="Please fill out this field.", status_code=200, msg_prefix='',
                              html=False)

    def test_editUserChangeUsername(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')
        self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)

        resp = self.client.post('/edit.html/test@test.com', {'fname': 'test_name', 'lname': 'test_lname',
                                                             'username': 'test1@test.com', 'password': '<PASSWORD>',
                                                             'role': 'Ta'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        updated_user = User.objects.get(username='test1@test.com')
        self.assertEqual(updated_user.username, 'test1@test.com')

    def test_editUserChangeFName(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')
        self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)

        resp = self.client.post('/edit.html/test@test.com', {'fname': 'new_name', 'lname': 'test_lname',
                                                             'username': 'test@test.com', 'password': '<PASSWORD>',
                                                             'role': 'Supervisor'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        updated_user = User.objects.get(username='test@test.com')
        self.assertEqual(updated_user.fname, "new_name")

    def test_editUserChangeLName(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')
        self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)

        resp = self.client.post('/edit.html/test@test.com', {'fname': 'test_name', 'lname': 'new_lname',
                                                             'username': 'test@test.com', 'password': '<PASSWORD>',
                                                             'role': 'Supervisor'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        updated_user = User.objects.get(username='test@test.com')
        self.assertEqual(updated_user.lname, 'new_lname')

    def test_editUserSkills(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')
        self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)

        resp = self.client.post('/edit.html/test@test.com', {'fname': 'test_name', 'lname': 'test_lname',
                                                             'username': 'test@test.com', 'password': '<PASSWORD>',
                                                             'role': 'Supervisor',
                                                             'java_skill': True, 'python_skill': True,
                                                             'frontend_skill': False,
                                                             'backend_skill': True, 'scala_skill': False,
                                                             'discrete_math_skill': False}, follow=True)
        self.assertEqual(resp.status_code, 200)
        updated_user = User.objects.get(username='test@test.com')
        self.assertEqual(updated_user.java_skill, True)
        self.assertEqual(updated_user.python_skill, True)


class LogoutTest(TestCase):
    client = None

    def test_logoutSupervisor(self):
        self.client.post('', {'username': 'test1@test', 'password': 'PASSWORD', 'role': 'Supervisor'})
        resp = self.client.post('/logout/', {'username': 'test1@test', 'password': 'PASSWORD'})
        self.assertEqual(resp.status_code, 405)

    def test_logoutInstructor(self):
        self.client.post('', {'username': 'test2@test', 'password': 'PASSWORD', 'role': 'Instructor'})
        resp = self.client.post('/logout/', {'username': 'test2@test', 'password': 'PASSWORD'})
        self.assertEqual(resp.status_code, 405)

    def test_logoutTA(self):
        self.client.post('', {'username': 'test3@test', 'password': 'PASSWORD', 'role': 'TA'})
        resp = self.client.post('/logout/', {'username': 'test3@test', 'password': 'PASSWORD'})
        self.assertEqual(resp.status_code, 405)

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

        resp = self.client.get('/edit.html/test@test.com', {'username': 'test@test.com', 'fname': 'test_name',
                                                            'lname': 'test_lname', 'role': 'Supervisor'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/edit.html/test@test.com', {'username': 'test1@test.com', 'fname': 'test_name',
                                                             'lname': 'test_lname', 'role': 'Supervisor'}, follow=True)
        updated_user = User.objects.get(username='test1@test.com')
        self.assertEqual(updated_user.username, 'test1@test.com')

    def test_badUsernameEdit(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')
        test_user = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/edit.html/test@test.com', {'username': 'test@test.com', 'password': 'test',
                                                            'fname': 'test_name', 'lname': 'test_lname',
                                                            'role': 'Supervisor'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/edit.html/test@test.com', {'username': 'test1@test.com', 'password': 'test',
                                                             'fname': 'test_name', 'lname': 'test_lname',
                                                             'role': 'Supervisor'}, follow=True)
        self.assertEqual(resp.context['message'], "Error when updating user")

    def test_badEmail(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')
        test_user = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/edit.html/test@test.com', {'username': 'test@test.com', 'password': 'test',
                                                            'fname': 'test_name', 'lname': 'test_lname',
                                                            'role': 'Supervisor'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/edit.html/test@test.com', {'username': 'testtest.com', 'password': 'test',
                                                             'fname': 'test_name', 'lname': 'test_lname',
                                                             'role': 'Supervisor'}, follow=True)

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

        resp = self.client.post('/edit.html/test1@test.com', {'username': 'test10@test', 'password': 'test',
                                                              'fname': 'test_name', 'lname': 'test_lname',
                                                              'role': 'Supervisor'}, follow=True)

        with self.assertRaises(User.DoesNotExist, msg="User does not exist"):
            user = User.objects.get(username='test10@test.com')

    def test_userEditOwnProfile(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='TA')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/edit.html/test@test.com', {'username': 'test@test.com', 'fname': 'test_name',
                                                            'lname': 'test_lname'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post('/edit.html/test@test.com', {'username': 'test1@test.com', 'fname': 'test_name',
                                                             'lname': 'test_lname'}, follow=True)
        updated_user = User.objects.get(username='test1@test.com')
        self.assertEqual(updated_user.username, 'test1@test.com')

    def test_editBadCourseName(self):
        test_course = Course.objects.create(Course_name="Math 101", Course_description="", MeetType="Online")
        test_course = Course.objects.create(Course_name="Math 100", Course_description="", MeetType="Online")
        test_user = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username': 'test1@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/edit.html/Math%20101', {'CourseName': 'Math 101', 'course_desc': '',
                                                         'MeetType': 'Online'})
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post('/edit.html/Math%20101', {'CourseName': 'Math 100', 'course_desc': '',
                                                          'MeetType': 'Online'})
        self.assertEqual(resp.context['message'], "There was an error updating the course")

    def test_badUserTryToEdit(self):
        test_course = Course.objects.create(Course_name="Math 100", Course_description="", MeetType="Online")
        test_user = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='TA')
        resp = self.client.post('', {'username': 'test1@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/edit.html/Math%20100', {'CourseName': 'Math 105', 'course_desc': '',
                                                          'MeetType': 'Online'})

        with self.assertRaises(Course.DoesNotExist, msg="Course does not exist"):
            course = Course.objects.get(Course_name='Math 105')

    def test_instructorRemovesTA(self):
        test_course = Course.objects.create(Course_name="Math 100", Course_description="", MeetType="Online")
        test_user = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='TA')
        user = User.objects.get(username='test1@test.com')
        test_user = User.objects.create(username='test2@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Instructor')
        start = datetime.strptime("2022-01-01 12:00:00", "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime("2023-01-01 12:00:00", "%Y-%m-%d %H:%M:%S")
        course = Course.objects.get(Course_name="Math 100")
        test_section = Section.objects.create(Course=course, section_number="401", LecLab="Lecture", start=start,
                                              end=end, credits=4, instructor=None, ta=user)

        resp = self.client.post('', {'username': 'test1@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(test_section.ta, user)
        url = '/remove_ta/' + str(test_section.id) + '/'
        resp = self.client.get(url, {'section_id': test_section.id})
        section = Section.objects.get(section_number="401")
        self.assertEqual(section.ta, None)

    def test_instructorEdit(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Instructor')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/edit.html/test@test.com', {'username': 'test@test.com', 'fname': 'test_name',
                                                            'lname': 'test_lname', 'role': 'Instructor'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/edit.html/test@test.com', {'username': 'test1@test.com', 'fname': 'test_name',
                                                             'lname': 'test_lname', 'role': 'Instructor'}, follow=True)
        updated_user = User.objects.get(username='test1@test.com')
        self.assertEqual(updated_user.username, 'test1@test.com')

class test_addCourse(TestCase):
    def setUp(self):
        self.client = Client()
        test_course = Course.objects.create(Course_name="Math 101", Course_description="", MeetType="Online")

    def test_addCourse(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/addcourse/', follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/addcourse/', {'CourseName': 'Math 100', 'coursedesc': '',
                                                'MeetType': 'Online'})
        self.assertEqual(resp.context['message'], "You have successfully added Math 100")
        course = Course.objects.get(Course_name="Math 100")

    def test_badCourseName(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/addcourse/', {'CourseName': 'Math 101', 'coursedesc': '', 'MeetType': 'Online'})
        self.assertEqual(resp.context['message'], "Course already exists")

    def test_badUserTriesToAddCourse(self):
        test_user = User.objects.create(username='test2@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='TA')

        resp = self.client.post('', {'username': 'test2@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/addcourse/', {'CourseName': 'Math 100', 'coursedesc': '', 'MeetType': 'Online'})

        with self.assertRaises(Course.DoesNotExist, msg="Course does not exist"):
            course = Course.objects.get(Course_name='Math 100')

    def test_ForgotRequiredData(self):
        test_user = User.objects.create(username='test2@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username': 'test2@test', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/addcourse/', follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/addcourse/', {'CourseName': "Math 100", 'coursedesc': "",
                                                'MeetType': ""})

        self.assertEqual(resp.context['message'], "Missing information")


class test_addSection(TestCase):
    def setUp(self):
        self.client = Client()
        start = "2022-01-01T12:00"
        end = "2023-01-01T12:00"
        test_course = Course.objects.create(Course_name="Math 101", Course_description="", MeetType="Online")
        course = Course.objects.get(Course_name="Math 101")
        Section.objects.create(Course=course, section_number="401", LecLab="Lecture", start=start,
                               end=end, credits=4, instructor=None, ta=None)

    def test_addSection(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/addsection/Math%20101', follow=True)
        self.assertEqual(resp.status_code, 200)

        course = Course.objects.get(Course_name="Math 101")
        start = "2022-01-01T12:00"
        end = "2023-02-02T12:00"

        resp = self.client.post('/addsection/Math%20101', {
            'course_name': course.Course_name,
            'sec_num': '402',
            'LecLab': 'Lecture',
            'start': start,
            'end': end,
            'credits': '4',
            'instructor': 'None',
            'ta': 'None'
        }, follow=True)
        section = Section.objects.get(section_number="402")
        self.assertEqual(resp.context['message'], "You have added 402 to Math 101")
        self.assertEqual(str(section.section_number), "402")

    def test_addBadStartDate(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/addsection/Math%20101', follow=True)
        self.assertEqual(resp.status_code, 200)

        course = Course.objects.get(Course_name="Math 101")
        start = "2024-01-01T12:00"
        end = "2023-02-02T12:00"
        resp = self.client.post('/addsection/Math%20101', {
            'course_name': course.Course_name,
            'sec_num': '402',
            'LecLab': 'Lecture',
            'start': start,
            'end': end,
            'credits': '4',
            'instructor': 'None',
            'ta': 'None'
        }, follow=True)
        self.assertEqual(resp.context['message'], "Cannot have start date/time after end")

    def test_addBadStartDate(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/addsection/Math%20101', follow=True)
        self.assertEqual(resp.status_code, 200)

        course = Course.objects.get(Course_name="Math 101")
        start = "2024-01-01T12:00"
        end = "2023-02-02T12:00"
        resp = self.client.post('/addsection/Math%20101', {
            'course_name': course.Course_name,
            'sec_num': '402',
            'LecLab': 'Lecture',
            'start': start,
            'end': end,
            'credits': '4',
            'instructor': 'None',
            'ta': 'None'
        }, follow=True)
        self.assertEqual(resp.context['message'], "Cannot have start date/time after end")

    def test_addBadSectionNumber(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/addsection/Math%20101', follow=True)
        self.assertEqual(resp.status_code, 200)

        course = Course.objects.get(Course_name="Math 101")
        start = "2022-01-01T12:00"
        end = "2023-02-02T12:00"
        resp = self.client.post('/addsection/Math%20101', {
            'course_name': course.Course_name,
            'sec_num': '401',
            'LecLab': 'Lecture',
            'start': start,
            'end': end,
            'credits': '4',
            'instructor': 'None',
            'ta': 'None'
        }, follow=True)
        self.assertEqual(resp.context['message'], "A section with this number already exists")

    def test_addBadUserAddsSection(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='TA')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        course = Course.objects.get(Course_name="Math 101")
        start = "2022-01-01T12:00"
        end = "2023-02-02T12:00"
        resp = self.client.post('/addsection/Math%20101', {
            'course_name': course.Course_name,
            'sec_num': '402',
            'LecLab': 'Lecture',
            'start': start,
            'end': end,
            'credits': '4',
            'instructor': 'None',
            'ta': 'None'
        }, follow=True)

        with self.assertRaises(Section.DoesNotExist, msg="Section does not exist"):
            Section.objects.get(section_number="402")

    def test_ForgetsRequiredData(self):
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='TA')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        course = Course.objects.get(Course_name="Math 101")
        start = "2022-01-01T12:00"
        end = "2023-02-02T12:00"
        resp = self.client.post('/addsection/Math%20101', {
            'course_name': course.Course_name,
            'sec_num': '',
            'LecLab': 'Lecture',
            'start': start,
            'end': end,
            'credits': '4',
            'instructor': 'None',
            'ta': 'None'
        }, follow=True)

        with self.assertRaises(Section.DoesNotExist, msg="Section does not exist"):
            Section.objects.get(section_number="402")

class deleteTests(TestCase):
    def setUp(self):
        self.client = Client()
        test_user = User.objects.create(username='test@test.com', password='test', fname='test_name',
                                        lname='test_lname', role='Supervisor')
        test_user2 = User.objects.create(username='test2@test.com', password='test', fname='test_name',
                                         lname='test_lname', role='TA')

    def test_deleteUser(self):
        test_user1 = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                         lname='test_lname', role='Supervisor')

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get('/delete.html/test1@test.com', follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/delete.html/test1@test.com', follow=True)
        with self.assertRaises(User.DoesNotExist, msg="User does not exist"):
            user = User.objects.get(username='testtest.com')

    def test_deleteSection(self):
        start = datetime.strptime("2022-01-01T12:00", "%Y-%m-%dT%H:%M")
        end = datetime.strptime("2023-01-01T12:00", "%Y-%m-%dT%H:%M")
        test_user1 = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                         lname='test_lname', role='Supervisor')

        test_course = Course.objects.create(Course_name="Math 101", Course_description="", MeetType="Online")
        course = Course.objects.get(Course_name="Math 101")

        test_section = Section.objects.create(Course=course, section_number="401", LecLab="Lecture", start=start,
                                              end=end, credits=4, instructor=None, ta=None)

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/deletesection/Math%20101/401/', follow=True)
        with self.assertRaises(Section.DoesNotExist, msg="Section does not exist"):
            section = Section.objects.get(Course=course.id)

    def test_badUserTriesToDeleteSection(self):
        start = datetime.strptime("2022-01-01T12:00", "%Y-%m-%dT%H:%M")
        end = datetime.strptime("2023-01-01T12:00", "%Y-%m-%dT%H:%M")
        test_user1 = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                         lname='test_lname', role='TA')

        test_course = Course.objects.create(Course_name="Math 101", Course_description="", MeetType="Online")
        course = Course.objects.get(Course_name="Math 101")

        test_section = Section.objects.create(Course=course, section_number="401", LecLab="Lecture", start=start,
                                              end=end, credits=4, instructor=None, ta=None)

        resp = self.client.post('', {'username': 'test1@test.com', 'password': 'test'}, follow=True)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post('/deletesection/Math%20101/401/', follow=True)
        section = Section.objects.get(section_number="401")
        self.assertEqual(str(section.section_number), "401")

    def test_deleteCourse(self):
        test_course = Course.objects.create(Course_name="Math 101", Course_description="", MeetType="Online")

        resp = self.client.post('', {'username': 'test@test.com', 'password': 'test'}, follow=True)

        resp.client.get('/delete.html/Math%20101', follow=True)
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post('/delete.html/Math%20101', follow=True)
        with self.assertRaises(Course.DoesNotExist, msg="Course does not exist"):
            course = Course.objects.get(Course_name='Math 101')

    def test_badUserTriesToDeleteCourse(self):
        test_course = Course.objects.create(Course_name="Math 101", Course_description="", MeetType="Online")

        resp = self.client.post('', {'username': 'test2@test.com', 'password': 'test'}, follow=True)

        resp = resp.client.post('/delete.html/Math%20101')
        course = Course.objects.get(Course_name='Math 101')
        self.assertEqual(course.Course_name, 'Math 101')

    def test_badUserTriesToDeleteUser(self):
        test_user1 = User.objects.create(username='test10@test.com', password='test', fname='test_name',
                                         lname='test_lname', role='Supervisor')
        resp = self.client.post('', {'username': 'test1@test.com', 'password': 'test'}, follow=True)

        resp = resp.client.post('/delete.html/test10@test.com', follow=True)
        user = User.objects.get(username='test10@test.com')

        self.assertEqual(user.username, 'test10@test.com')

    def test_deleteCourseRemovesSections(self):
        start = datetime.strptime("2022-01-01T12:00", "%Y-%m-%dT%H:%M")
        end = datetime.strptime("2023-01-01T12:00", "%Y-%m-%dT%H:%M")
        test_user1 = User.objects.create(username='test1@test.com', password='test', fname='test_name',
                                         lname='test_lname', role='Supervisor')

        test_course = Course.objects.create(Course_name="Math 101", Course_description="", MeetType="Online")
        course = Course.objects.get(Course_name="Math 101")

        test_section = Section.objects.create(Course=course, section_number="401", LecLab="Lecture", start=start,
                                              end=end, credits=4, instructor=None, ta=None)
        resp = self.client.post('/', {'username': 'test1@test.com', 'password': 'test'})

        resp = self.client.post('/delete.html/Math%20101')
        with self.assertRaises(Section.DoesNotExist, msg="Section does not exist"):
            section = Section.objects.get(section_number='401')


class LogoutTest(TestCase):
    pass
