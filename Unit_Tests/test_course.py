from django.test import TestCase
from classes.CourseClass import Course
from classes.TAClass import TAClass


class CourseTest(TestCase):
    def setUp(self):
        # Setting up a Course object for use in all test methods
        self.ta = TAClass("test", "Name", "Test", "password", "test@example.com")
        self.wrongta = TAClass("wrong", "Name", "Test", "password", "test@example.com")

        self.course = Course("Computer Science", "101", "09:00 AM", "10:30 AM", 4, "Dr. Smith", ta=self.ta)

    def test_get_name(self):
        self.assertEqual(self.course.get_name(), "Computer Science")

    def test_wrong_name(self):
        self.assertNotEqual(self.course.get_name(), "Computer Architecture")

    def test_get_section(self):
        self.assertEqual(self.course.get_section(), "101")

    def test_wrong_section(self):
        self.assertNotEqual(self.course.get_section(), "100")

    def test_get_start(self):
        self.assertEqual(self.course.get_start(), "09:00 AM")

    def test_wrong_start(self):
        self.assertNotEqual(self.course.get_start(), "09:30 AM")

    def test_get_end(self):
        self.assertEqual(self.course.get_end(), "10:30 AM")

    def test_wrong_end(self):
        self.assertNotEqual(self.course.get_end(), "09:30 AM")

    def test_get_credits(self):
        self.assertEqual(self.course.get_credits(), 4)

    def test_wrong_credits(self):
        self.assertNotEqual(self.course.get_credits(), 3)

    def test_get_instructor(self):
        self.assertEqual(self.course.get_instructor(), "Dr. Smith")

    def test_wrong_instructor(self):
        self.assertNotEqual(self.course.get_instructor(), "Dr. Johnson")

    def test_get_ta(self):
        self.assertEqual(self.course.get_ta(), self.ta)

    def test_wrong_ta(self):
        self.assertNotEqual(self.course.get_ta(), self.wrongta)


