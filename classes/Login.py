from ta_app.models import User

class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getUsername(self):
        user = self.findUser(self.username, self.password)
        return user.username

    def getPassword(self):
        user = self.findUser(self.username, self.password)
        return user.password

    def getRole(self):
        user = self.findUser(self.username, self.password)
        if user is not None:
            return user.role
        return None

    def findUser(self, username, password):
        try:
            user = User.objects.get(username=username)
            check = (user.password == password)
            if check:
                return user
            return None
        except Exception:
            return None


