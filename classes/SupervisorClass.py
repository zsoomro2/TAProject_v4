from classes.TAClass import TAClass
class Supervisor:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def createTA(self, username, password, fname, lname):
        ta_instance = TAClass(username, password, fname, lname)
        return ta_instance.save_details()

    """def createInstructor(self, username, password, fname, lname):
        instructor_instance = InstructorClass(username, password, fname, lname)
        return instructor_instance.save_details()"""

    def removeUser(self, username):
        pass

    def createCourse(self, Course_name, section, start, end, credits, instructor, ta):
        pass

    def removeCourse(self, section):
        pass
