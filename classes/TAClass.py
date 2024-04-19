from ta_app.models import User
class TAClass(object):
    def __init__(self, username, password, fname, lname):
        self.username = username
        self.password = password
        self.fname = fname
        self.lname = lname
        self.role = "TA"

    def editInfo(self, username):
        pass

    def save_details(self):
        ta = User.objects.create(username=self.username, password=self.password, fname=self.fname, lname=self.lname,
                                 role=self.role)
