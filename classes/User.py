class User:

    def __init__(self, request, username, password, firstName, lastName, phone, role):
        self.username = username
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone
        self.role = role

        self.session = request.session
        user = self.session.get('session_key')
        if 'session_key' not in request.session:
            user = self.session['session_key'] = {}
        self.user = user

    def get_username(self):
        return self.username

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