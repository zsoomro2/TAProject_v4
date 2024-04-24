import unittest
from ta_app.models import User, Course

from classes.Instructor import Instructor


class InstructorTestAssign(unittest.TestCase):
    def setUp(self):
        self.instructor = User.objects.create(
            username='instructor@example.com',
            password='instructor123',
            fname='Jane',
            lname='Smith',
            role='Instructor')

        self.ta = User.objects.create(
            username='ta@example.com',
            password='ta123',
            fname='Tom',
            lname='Jones',
            role='TA'
        )
        self.course = Course.objects.create(
            Course_name='math',
            section='101',
            start='feb2',
            end='feb3',
            credits='3',
            instructor='Jane',
            ta='')

    def test_assign_ta(self):
        # Test the assignTA method

        self.instructor.assignTA('math', 'Tom')

        assigned_ta = self.instructor.getAssignedTA('math')
        self.assertEqual(assigned_ta, "Tom")

    def test_assign_taNoCorse(self):
        try:
            self.instructor.assignTA('', 'Tom')
        except Exception as e:
            self.assertRaises(e, msg="Invalid username or password")

    def test_assign_taCorseNoName(self):
        try:
            self.instructor.assignTa('math', '')
        except Exception as e:
            self.assertRaises(e, msg="no course provided")

    def test_assign_nothing(self):
        try:
            self.instructor.assignTa('', '')
        except Exception as e:
            self.assertRaises(e, msg="nothing provided")


class InstructorTestEditInfo(unittest.TestCase):
    def setUp(self):
        self.instructor = User.objects.create(
            username='instructor@example.com',
            password='instructor123',
            fname='Jane',
            lname='Smith',
            role='Instructor')

        self.ta = User.objects.create(
            username='ta@example.com',
            password='ta123',
            fname='Tom',
            lname='Jones',
            role='TA'
        )
        self.course = Course.objects.create(
            Course_name='math',
            section='101',
            start='feb2',
            end='feb3',
            credits='3',
            instructor='Jane',
            ta='')

