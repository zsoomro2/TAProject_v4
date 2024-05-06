from classes.User import MyUser

def user(request):
    return {'user': MyUser(request, MyUser.get_username, MyUser.get_password, MyUser.get_firstName, MyUser.get_lastName,
                         MyUser.get_phone, MyUser.get_role)}