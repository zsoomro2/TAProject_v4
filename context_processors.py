from classes.User import User

def user(request):
    return {'user': User(request, User.get_username, User.get_password, User.get_firstName, User.get_lastName,
                         User.get_phone, User.get_role)}