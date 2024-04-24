from classes.CourseClass import Course
from classes.TAClass import TAClass
from classes.InstructorClass import Instructor


class Supervisor:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.courses = []
        self.tas = {}
        self.instructors = {}

    def createTA(self, username, password, fname, lname, email):
        if username in self.tas:
            raise ValueError("TA already exists.")
        ta_instance = TAClass(username, password, fname, lname, email)
        self.tas[username] = ta_instance
        return ta_instance

    def createInstructor(self, username, password, fname, lname):
        instructor_instance = Instructor(username, password, fname, lname)
        self.instructors[username] = instructor_instance
        return instructor_instance

    def removeTA(self, username):
        if username not in self.tas:
            raise ValueError("TA does not exist.")
        del self.tas[username]

    def removeInstructor(self, username):
        if username not in self.instructors:
            raise ValueError("Instructor does not exist.")
        del self.instructors[username]

    def createCourse(self, course_name, section, start, end, credits, instructor, ta):
        existing_course = next((c for c in self.courses if c.section == section), None)
        if existing_course:
            raise ValueError("Course already exists.")
        course_instance = Course(course_name, section, start, end, credits, instructor, ta)
        self.courses.append(course_instance)
        return course_instance

    def removeCourse(self, section):
        course_to_remove = next((c for c in self.courses if c.section == section), None)
        if not course_to_remove:
            raise ValueError("Course does not exist.")
        self.courses.remove(course_to_remove)
