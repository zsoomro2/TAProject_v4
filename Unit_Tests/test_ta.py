from django.test import TestCase
from ta_app.models import User
from classes.TAClass import TAClass


class TATestCase(TestCase):
    def setUp(self):
        self.ta_user = User.objects.create(username="ta@example.com", password="password", fname="TA", lname="User",
                                           role="TA")
        self.ta = TAClass(self.ta_user.username, self.ta_user.fname, self.ta_user.lname, self.ta_user.password,
                          self.ta_user.username)

    def test_username(self):
        self.assertEqual(self.ta.username, "ta@example.com")

    def test_fname(self):
        self.assertEqual(self.ta.fname, "TA")

    def test_lname(self):
        self.assertEqual(self.ta.lname, "User")

    def test_password(self):
        self.assertEqual(self.ta.password, "password")

    def test_email(self):
        self.assertEqual(self.ta.email, "ta@example.com")

    def test_courses(self):
        self.assertEqual(len(self.ta.courses), 0)

    def test_edit_info(self):
        ta = TAClass(self.ta_user.username, self.ta_user.fname, self.ta_user.lname, self.ta_user.password,
                     self.ta_user.username)

        ta.editInfo(fname="Updated", lname="TA")
        self.assertEqual(ta.fname, "Updated")
        self.assertEqual(ta.lname, "TA")

    def test_view_assignments_empty(self):
        ta = TAClass(self.ta_user.username, self.ta_user.fname, self.ta_user.lname, self.ta_user.password,
                     self.ta_user.username)

        assignments = ta.view_assignments()
        self.assertEqual(assignments, None)

    def test_view_assignments_with_courses(self):
        ta = TAClass(self.ta_user.username, self.ta_user.fname, self.ta_user.lname, self.ta_user.password,
                     self.ta_user.username)
        ta.courses = ["Course1", "Course2"]

        assignments = ta.view_assignments()
        self.assertEqual(assignments, ["Course1", "Course2"])
