from django.test import TestCase
from classes.CourseClass import Course
from classes.TAClass import TAClass


class InstructorTest(TestCase):
    def setUp(self):
        # Setting up a Course object for use in all test methods
        self.ta = TAClass("test", "Name", "Test", "password", "test@example.com")

        self.course = Course("Computer Science", "101", "09:00 AM", "10:30 AM", 4, "Dr. Smith", ta=self.ta)

    def test_get_name(self):
        self.assertEqual(self.course.get_name(), "Computer Science")

    def test_get_section(self):
        self.assertEqual(self.course.get_section(), "101")

    def test_get_start(self):
        self.assertEqual(self.course.get_start(), "09:00 AM")

    def test_get_end(self):
        self.assertEqual(self.course.get_end(), "10:30 AM")

    def test_get_credits(self):
        self.assertEqual(self.course.get_credits(), 4)

    def test_get_instructor(self):
        self.assertEqual(self.course.get_instructor(), "Dr. Smith")

    def test_get_ta(self):
        self.assertEqual(self.course.get_ta(), self.ta)
