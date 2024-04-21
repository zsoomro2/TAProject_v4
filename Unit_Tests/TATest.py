from django.test import TestCase
from ta_app.models import User, Course, Roles
from classes import TAClass


class TATestCase(TestCase):
    def setUp(self):
        self.ta_user = User.objects.create(username="ta@example.com", password="password", fname="TA", lname="User",
                                           role=Roles.TA)
        self.instructor_user = User.objects.create(username="instructor@example.com", password="password",
                                                   fname="Instructor", lname="User", role=Roles.Instructor)
        self.course = Course.objects.create(
            Course_name="Calculus",
            section=1,
            start="2022-09-01",
            end="2023-06-01",
            credits=3,
            instructor=self.instructor_user,
            ta=self.ta_user
        )

    def test_view_assignments(self):
        ta = TAClass.TAClass(self.ta_user.id)
        assignments = ta.view_assignments()
        self.assertEqual(assignments.first(), self.course)

    def test_update_info(self):
        ta = TAClass.TAClass(self.ta_user.id)
        updated = ta.editInfo(fname="Updated", lname="TA")
        self.ta_user.refresh_from_db()
        self.assertEqual(self.ta_user.fname, "Updated")
        self.assertEqual(self.ta_user.lname, "TA")
