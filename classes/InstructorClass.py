class Instructor:
    def __init__(self, user_id, password, fname, lname):
        self.username = user_id
        self.password = password
        self.fname = fname
        self.lname = lname
        self.ta_assignments = {}

    def editInfo(self, fname, lname):
        self.fname = fname
        self.lname = lname

    def assignTA(self, course, ta_name):
        self.ta_assignments[course] = ta_name

    def getAssignedTA(self, course):
        return self.ta_assignments.get(course, None)
