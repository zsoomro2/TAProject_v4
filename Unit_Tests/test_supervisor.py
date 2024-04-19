from django.test import TestCase
from classes.SupervisorClass import Supervisor
from classes.TAClass import TAClass
from ta_app.models import User, Course
import unittest

class TestSupervisor(TestCase):
    def test_init(self):
        self.supervisor = Supervisor("user", "password")
        assert self.supervisor is not None

    def test_add_supervisor(self):
        self.supervisor = Supervisor("user", "password")
        self.assertEqual(self.supervisor.username, "user")

class TestCreateUser(TestCase):
    def setUp(self):
        self.supervisor = Supervisor("user", "password")
        self.jack = TAClass("jdue", "due", "Jack", "Due")
        self.noah = TAClass("nsprunk", "sprunk", "Noah", "Sprunk")
        self.john = InstructorClass("jboyland", "boyland", "John", "Boyland")

    def test_create_user(self):
        self.test = Supervisor.createTA(self.supervisor, "jdue", "due", "Jack", "Due")
        self.assertEqual(self.test, self.jack)

    def test_create_instructor(self):
        self.test = Supervisor.createInstructor(self.supervisor, "jboyland", "boyland", "John", "Boyland")
        self.assertEqual(self.test, self.john)

    def test_remove_user(self):
        Supervisor.removeUser(self.supervisor, self.jack.username)
        users = list(User.objects.filter(role="TA"))
        self.assertEqual(len(users), 1)

    def test_create_course(self):
        self.test = Supervisor.createCourse(self.supervisor, "Software Engineering", 337, "01/20/23", "05/20/24", 3,
                                            self.john, self.jack)
        courses = list(Course.objects.filter(Course_name="Software Engineering"))
        self.assertEqual(len(courses), 1)

    def test_remove_course(self):
        Supervisor.removeCourse(self.supervisor, 337)
        courses = list(Course.objects.filter(section=337))
        self.assertEqual(len(courses), 0)