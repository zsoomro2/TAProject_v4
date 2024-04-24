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
        self.jack = TAClass("jdue", "due", "Jack", "Due")
        self.john = InstructorClass("jboyland", "boyland", "John", "Boyland")
        self.john = Instructor("jboyland", "boyland", "John", "Boyland")

    def test_create_ta(self):
        self.test = Supervisor.createTA(self.supervisor, "jdue", "due", "Jack", "Due")
        self.assertEqual(self.test, self.jack)

    def test_create_instructor(self):
        self.test = Supervisor.createInstructor(self.supervisor, "jboyland", "boyland", "John", "Boyland")
        self.assertEqual(self.test, self.john)

    def test_create_course(self):
        self.test = Supervisor.createCourse(self.supervisor, "Software Engineering", 361, "01/20/23", "05/20/24", 3,
                                            self.john, self.jack)
        courses = list(Course.objects.filter(Course_name="Software Engineering"))
        self.assertEqual(len(courses), 1)

class TestRemove(TestCase) :
    def setUp(self):
        self.supervisor = Supervisor("user", "password")
        self.jack = TAClass("jdue", "due", "Jack", "Due")
        self.john = InstructorClass("jboyland", "boyland", "John", "Boyland")

class TestRemove(TestCase):
    def setUp(self):
        self.supervisor = Supervisor("user", "password")
        self.jack = TAClass("jdue", "due", "Jack", "Due")
        self.john = Instructor("jboyland", "boyland", "John", "Boyland")
        Supervisor.createTA(self.supervisor, "jdue", "due", "Jack", "Due")
        Supervisor.createInstructor(self.supervisor, "jboyland", "boyland", "John", "Boyland")
        Supervisor.createCourse(self.supervisor, "Software Engineering", 361, "01/20/23", "05/20/24", 3,
                                self.john, self.jack)

    def test_remove_TA(self):
        Supervisor.removeTA(self.supervisor, self.jack.username)
        users = list(User.objects.filter(role="TA"))
        self.assertEqual(len(users), 0)

    def test_remove_instructor(self):
        Supervisor.removeTA(self.supervisor, self.john.username)
        users = list(User.objects.filter(role="Instructor"))
        self.assertEqual(len(users), 0)

    def test_remove_unknown_TA(self):
        self.assertFalse(Supervisor.removeTA(self.supervisor, "jim"))

    def test_remove_unknown_instructor(self):
        self.assertFalse(Supervisor.removeTA(self.supervisor, "jayson"))

    def test_remove_course(self):
        Supervisor.removeCourse(self.supervisor, 361)
        courses = list(Course.objects.filter(section=361))
        self.assertEqual(len(courses), 0)

    def test_remove_unknown_course(self):
        self.assertFalse(Supervisor.removeCourse(self.supervisor, 360))
