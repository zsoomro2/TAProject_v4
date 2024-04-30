class User:

    def __init__(self, username, password, firstName, lastName, phone, role):
        self.username = username
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.role = role

    def get_username(self):
        return self.uesername

    def get_password(self):
        return self.password

    def get_firstName(self):
        return self.firstName

    def get_lastName(self):
        return self.lastName

    def get_phone(self):
        return self.phone

    def get_role(self):
        return self.role