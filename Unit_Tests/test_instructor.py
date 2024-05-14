from django.test import TestCase
from classes.InstructorClass import Instructor


class InstructorTest(TestCase):
    def setUp(self):
        self.instructor = Instructor(user_id='Bob', password=1, fname='Bob', lname='Tob')

    def test_user_id(self):
        self.assertEqual(self.instructor.username, 'Bob')

    def test_password(self):
        self.assertEqual(self.instructor.password, 1)

    def test_name(self):
        self.assertEqual(self.instructor.fname, 'Bob')
        self.assertEqual(self.instructor.lname, 'Tob')

    def test_assign_ta(self):
        # Test the assignTA method
        course = "Introduction to Programming"
        ta_name = "Tom"

        self.instructor.assignTA(course, ta_name)
        assigned_ta = self.instructor.getAssignedTA(course)
        self.assertEqual(assigned_ta, ta_name)

    def test_edit_info(self):
        # Assuming editInfo changes the instructor's name attribute
        old_name = self.instructor.username
        self.instructor.editInfo('John', 'Smith')
        self.assertEqual(self.instructor.fname, 'John')

    def test_delete_info(self):
        self.instructor.editInfo(None, None)
        self.assertEqual(self.instructor.fname, None)
        self.assertEqual(self.instructor.lname, None)

    def test_get_assigned_ta(self):
        self.instructor.assignTA('Intro to Programming', 'John Doe')
        ta_name = self.instructor.getAssignedTA('Intro to Programming')
        self.assertEqual(ta_name, 'John Doe')

    def test_no_assigned_ta(self):
        ta_name = self.instructor.getAssignedTA('Intro to Programming')
        self.assertEqual(ta_name, None)

    def test_ta_in_course(self):
        course_name = "Calculus 101"
        ta_name = "John Doe"

        self.instructor.assignTA(course_name, ta_name)
        self.assertIn(course_name, self.instructor.ta_assignments)
        self.assertEqual(self.instructor.ta_assignments[course_name], ta_name)

    def test_assigned_none_ta(self):
        course_name = "Calculus 101"
        ta_name = None

        self.instructor.assignTA(course_name, ta_name)
        self.assertEqual(self.instructor.ta_assignments[course_name], ta_name)


