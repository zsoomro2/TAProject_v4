from ta_app.models import User
from ta_app.models import Roles


class AddUser:
    def __init__(self, username, password, fname, lname, role):
        self.username = username
        self.password = password
        self.fname = fname
        self.lname = lname
        self.role = role

    def validate(self):
        data_list = [self.username, self.password, self.fname, self.lname, self.role]
        if len(data_list) == 5:
            for item in data_list:
                if item == "" or item is None or self.role not in Roles:
                    return False
            char_list = list(self.username)
            for char in char_list:
                if char == '@':
                    return True
        return False

    def checkUser(self):
        try:
            check = User.objects.get(username=self.username)
            return True
        except Exception:
            return False
