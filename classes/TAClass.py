class TAClass:
    def __init__(self, username, lname, fname, password, email):
        self.username = username
        self.lname = lname
        self.fname = fname
        self.password = password
        self.email = email
        self.courses = []

    def view_assignments(self):
        pass

    def editInfo(self, fname=None, lname=None, email=None):
        self.fname = fname
        self.lname = lname
        self.email = email
