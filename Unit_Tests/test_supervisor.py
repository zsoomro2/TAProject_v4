from django.test import TestCase
from classes.SupervisorClass import Supervisor
from classes.TAClass import TAClass
from ta_app.models import User, Course
import unittest
from classes.InstructorClass import Instructor


class TestSupervisor(TestCase):
    def test_init(self):
        self.supervisor = Supervisor("user", "password")
        assert self.supervisor is not None

    def test_add_supervisor(self):
        self.supervisor = Supervisor("user", "password")
        self.assertEqual(self.supervisor.username, "user")


class TestCreate(TestCase):
    def setUp(self):
        self.supervisor = Supervisor("user", "password")
        self.jack = TAClass("jdue", "due", "Jack", "Due", "admin@admin.com")
        self.john = Instructor("jboyland", "boyland", "John", "Boyland")
        self.john = Instructor("jboyland", "boyland", "John", "Boyland")

    def test_create_ta(self):
        self.test = Supervisor.createTA(self.supervisor, "jdue", "Jack", "Due", "password", "admin@admin.com")
        self.assertEqual(self.test.username, "jdue")
        self.assertEqual(self.test.fname, "Jack")
        self.assertEqual(self.test.lname, "Due")
        self.assertEqual(self.test.email, "admin@admin.com")

    def test_create_instructor(self):
        self.test = self.supervisor.createInstructor("jboyland", "boyland", "John", "Boyland")
        self.assertEqual(self.test.fname, "John")
        self.assertEqual(self.test.lname, "Boyland")
        self.assertEqual(self.test.username, "jboyland")
        self.assertEqual(self.test.password, "boyland")

    def test_create_course_successfully(self):
        instructor = self.supervisor.createInstructor("instusername", "instpassword", "Jane", "Doe")
        ta = self.supervisor.createTA("tausername", "tapassword", "John", "Doe", "john.doe@example.com")
        course = self.supervisor.createCourse("Software Engineering", 361, "01/20/23", "05/20/24", 3, instructor, ta)
        self.assertIn(course, self.supervisor.courses)
        self.assertEqual(course.name, "Software Engineering")

    def test_create_course_failure(self):
        instructor = self.supervisor.createInstructor("instusername", "instpassword", "Jane", "Doe")
        ta = self.supervisor.createTA("tausername", "tapassword", "John", "Doe", "john.doe@example.com")
        self.supervisor.createCourse("Software Engineering", 361, "01/20/23", "05/20/24", 3, instructor, ta)
        with self.assertRaises(ValueError):
            self.supervisor.createCourse("Software Engineering", 361, "01/20/23", "05/20/24", 3, instructor, ta)


class TestRemove(TestCase):
    def setUp(self):
        self.supervisor = Supervisor("user", "password")
        self.jack = TAClass("jdue", "due", "Jack", "Due")
        self.john = Instructor("jboyland", "boyland", "John", "Boyland")


class TestRemove(TestCase):
    def setUp(self):
        self.supervisor = Supervisor("user", "password")
        self.jack = TAClass("jdue", "due", "Jack", "Due", "admin@admin.com")
        self.john = Instructor("jboyland", "boyland", "John", "Boyland")
        Supervisor.createTA(self.supervisor, "jdue", "due", "Jack", "Due", "admin@admin.com")
        Supervisor.createInstructor(self.supervisor, "jboyland", "boyland", "John", "Boyland")
        Supervisor.createCourse(self.supervisor, "Software Engineering", 361, "01/20/23", "05/20/24", 3,
                                self.john, self.jack)

    def test_remove_TA(self):
        Supervisor.removeTA(self.supervisor, self.jack.username)
        users = list(User.objects.filter(role="TA"))
        self.assertEqual(len(users), 0)

    def test_remove_instructor(self):
        self.supervisor.createInstructor(self.john.username, "password", self.john.fname, self.john.lname)
        self.supervisor.removeInstructor(self.john.username)
        self.assertNotIn(self.john.username, self.supervisor.instructors)

    def test_remove_unknown_TA(self):
        with self.assertRaises(ValueError) as context:
            self.supervisor.removeTA("jim")
        self.assertEqual(str(context.exception), "TA does not exist.")

    def test_remove_unknown_instructor(self):
        with self.assertRaises(ValueError) as context:
            self.supervisor.removeInstructor("jayson")
        self.assertEqual(str(context.exception), "Instructor does not exist.")

    def test_remove_course(self):
        Supervisor.removeCourse(self.supervisor, 361)
        courses = list(Course.objects.filter(section=361))
        self.assertEqual(len(courses), 0)

    def test_remove_unknown_course(self):
        with self.assertRaises(ValueError) as context:
            self.supervisor.removeCourse(360)
        self.assertEqual(str(context.exception), "Course does not exist.")
