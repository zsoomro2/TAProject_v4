from django.test import TestCase
from classes.TAClass import TAClass  # Make sure to adjust the import path based on your project structure


class TATest(TestCase):
    def setUp(self):
        self.ta = TAClass(username="testname", lname="Name", fname="Test", password="password",
                          email="test@example.com")

    def test_username(self):
        self.assertEqual(self.ta.username, "testname")

    def test_lname(self):
        self.assertEqual(self.ta.lname, "Name")

    def test_fname(self):
        self.assertEqual(self.ta.fname, "Test")
        self.assertEqual(self.ta.password, "password")
        self.assertEqual(self.ta.email, "test@example.com")
        self.assertEqual(len(self.ta.courses), 0)

    def test_view_assignments(self):
        self.assertIsNone(self.ta.view_assignments(),
                          "view_assignments should return None or similar for no assignments")
