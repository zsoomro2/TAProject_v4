from ta_app.models import User

class Login:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password

    def getRole(self):
        return self.role