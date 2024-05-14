from django.test import TestCase, RequestFactory
from ta_app.models import User, Course
from classes.EditClass import EditClass


class EditTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test@test.com', password='<PASSWORD>', fname='test', lname='test_lname', role='TA')
        self.course = Course.objects.create(Course_name='test', Course_description='test', MeetType='InPerson')

        self.edituser = EditClass(self.user, 'test@test.com')
        self.editcourse = EditClass(self.course, 'test')

    def test_isUser(self):
        self.assertEqual(self.edituser.isUser(), True)

    def test_isCourse(self):
        self.assertEqual(self.editcourse.isCourse(), True)

class UpdateUserTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.user = User.objects.create(
            username='test@test.com',
            password='<PASSWORD>',
            fname='John',
            lname='Doe',
            role='TA',
            java_skill=False,
            python_skill=False,
            frontend_skill=False,
            backend_skill=False,
            scala_skill=False,
            discrete_math_skill=False
        )

    def test_update_user_success(self):
        request = self.factory.post('/edit.html/test@test.com', {
            'username': 'test2@test.com',
            'fname': 'Jane',
            'lname': 'Smith',
            'role': 'Instructor',
            'java_skill': True,
        })

        edit_instance = EditClass(request, 'test@test.com')
        result = edit_instance.updateUser(request, 'test@test.com')

        user = User.objects.get(username='test2@test.com')

        self.assertTrue(result)
        self.assertEqual(user.username, 'test2@test.com')
        self.assertEqual(user.fname, 'Jane')
        self.assertEqual(user.lname, 'Smith')
        self.assertEqual(user.role, 'Instructor')
        self.assertTrue(user.java_skill)
        self.assertFalse(user.python_skill)
        self.assertFalse(user.frontend_skill)
        self.assertFalse(user.backend_skill)
        self.assertFalse(user.scala_skill)
        self.assertFalse(user.discrete_math_skill)

    def test_update_user_no_changes(self):
        request = self.factory.post('/edit.html/test@test.com', {
            'username': 'test@test.com'
        })

        edit_instance = EditClass(request, 'test@test.com')
        result = edit_instance.updateUser(request, 'test@test.com')

        user = User.objects.get(username='test@test.com')

        self.assertTrue(result)
        self.assertEqual(user.fname, 'John')
        self.assertEqual(user.lname, 'Doe')
        self.assertEqual(user.role, 'TA')
        self.assertFalse(user.java_skill)
        self.assertFalse(user.python_skill)
        self.assertFalse(user.frontend_skill)
        self.assertFalse(user.backend_skill)
        self.assertFalse(user.scala_skill)
        self.assertFalse(user.discrete_math_skill)

    def test_update_user_partial_changes(self):
        request = self.factory.post('/edit.html/test@test.com', {
            'username': 'test@test.com',
            'fname': 'Jane',
            'python_skill': True,
            'frontend_skill': True,
        })

        edit_instance = EditClass(request, 'test@test.com')
        result = edit_instance.updateUser(request, 'test@test.com')

        user = User.objects.get(username='test@test.com')

        self.assertTrue(result)
        self.assertEqual(user.fname, 'Jane')
        self.assertEqual(user.lname, 'Doe')
        self.assertEqual(user.role, 'TA')
        self.assertFalse(user.java_skill)
        self.assertTrue(user.python_skill)
        self.assertTrue(user.frontend_skill)
        self.assertFalse(user.backend_skill)
        self.assertFalse(user.scala_skill)
        self.assertFalse(user.discrete_math_skill)

    def test_update_user_nonexistent_user(self):
        request = self.factory.post('/edit.html/test@test.com', {
            'username': 'test@test.com',
            'fname': 'Jane',
        })

        edit_instance = EditClass(request, 'nonexistentuser')
        result = edit_instance.updateUser(request, 'nonexistentuser')

        self.assertFalse(result)

class UpdateCourseTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.course = Course.objects.create(
            Course_name='test',
            Course_description='test description',
            MeetType='In Person'
        )
        self.course2 = Course.objects.create(
            Course_name='test2',
            Course_description='test description',
            MeetType='Hybrid'
        )

    def test_update_course_success(self):
        request = self.factory.post('/edit.html/test', {
            'CourseName': 'UpdatedCourse',
            'MeetType': 'Hybrid',
            'course_desc': 'Updated description'
        })

        edit_instance = EditClass(request, 'test')
        result = edit_instance.updateCourse('test')

        course = Course.objects.get(Course_name='UpdatedCourse')

        self.assertTrue(result)
        self.assertEqual(course.Course_name, 'UpdatedCourse')
        self.assertEqual(course.MeetType, 'Hybrid')
        self.assertEqual(course.Course_description, 'Updated description')

    def test_update_course_name_conflict(self):
        request = self.factory.post('/edit.html/test', {
            'CourseName': 'test2',
            'MeetType': 'Hybrid',
            'course_desc': 'Updated description'
        })

        edit_instance = EditClass(request, 'test')
        result = edit_instance.updateCourse('test')

        self.assertFalse(result)

    def test_update_course_no_changes(self):
        request = self.factory.post('/edit.html/test', {
            'CourseName': 'test',
            'MeetType': 'In Person',
            'course_desc': 'test description'
        })

        edit_instance = EditClass(request, 'test')
        result = edit_instance.updateCourse('test')

        course = Course.objects.get(Course_name='test')

        self.assertTrue(result)
        self.assertEqual(course.Course_name, 'test')
        self.assertEqual(course.MeetType, 'In Person')
        self.assertEqual(course.Course_description, 'test description')

    def test_update_course_partial_changes(self):
        request = self.factory.post('/edit.html/test', {
            'CourseName': 'test',
            'MeetType': 'Hybrid',
            'course_desc': 'Updated description'
        })

        edit_instance = EditClass(request, 'test')
        result = edit_instance.updateCourse('test')

        course = Course.objects.get(Course_name='test')

        self.assertTrue(result)
        self.assertEqual(course.Course_name, 'test')
        self.assertEqual(course.MeetType, 'Hybrid')
        self.assertEqual(course.Course_description, 'Updated description')







