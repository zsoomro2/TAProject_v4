import unittest;

from classes.Instructor import Instructor


class instructorTest(unittest.TestCase):
    def setUp(self):
        self.instructor = Instructor()

    def test_assign_ta(self):
        # Test the assignTA method
        course = "Introduction to Programming"
        ta_name = "Tom"


        self.instructor.assignTA(course, ta_name)


        assigned_ta = self.instructor.getAssignedTA(course)
        self.assertEqual(assigned_ta, ta_name)