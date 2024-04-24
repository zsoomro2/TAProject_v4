from django.test import TestCase
from classes.InstructorClass import Instructor


class InstructorTest(TestCase):
    def setUp(self):
        self.instructor = Instructor(user_id='Bob', password=1)

    def test_assign_ta(self):
        # Test the assignTA method
        course = "Introduction to Programming"
        ta_name = "Tom"

        self.instructor.assignTA(course, ta_name)

        assigned_ta = self.instructor.getAssignedTA(course)
        self.assertEqual(assigned_ta, ta_name)

