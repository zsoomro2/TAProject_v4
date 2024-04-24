class TAClass:
    def __init__(self, username, fname, lname, password, email):
        self.username = username
        self.lname = lname
        self.fname = fname
        self.password = password
        self.email = email
        self.courses = []

    def view_assignments(self):
        if not self.courses:
            return None
        return self.courses

    def editInfo(self, fname=None, lname=None):
        self.fname = fname
        self.lname = lname
