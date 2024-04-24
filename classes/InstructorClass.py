class InstructorClass:
    def __init__(self, lname, fname, password, email):
        self.username = email
        self.lname = lname
        self.fname = fname
        self.password = password
        self.email = email
        self.courses = []

    def editInfo(self, name):
        pass

    def assignTA(self, course, ta_name):
        pass

    def getAssignedTA(self, course):
        pass
