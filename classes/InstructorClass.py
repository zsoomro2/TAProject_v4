class InstructorClass:
    def __init__(self, username, lname, fname, password, email):
        self.username = username
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
