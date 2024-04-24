from django.shortcuts import render, redirect
from django.views import View
from .models import User, Roles
from classes.Login import Login
from classes.AddUser import AddUser
from django.http import HttpResponseRedirect


# Create your views here.

class login(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        user = Login(request.POST['username'], request.POST['password'])
        user_obj = user.findUser(user.username, user.password)

        # create user_obj to grab a user/None type
        if user_obj is not None:
            if user.getRole() == "Supervisor":
                user_list = User.objects.filter(username=user.username)
                return render(request, 'supervisor.html',
                              {'message': "You have logged in", 'user_list': user_list})

            elif user.getRole() == "Instructor":
                user_list = User.objects.filter(username=user.username)
                return render(request, 'instructor.html',
                              {'message': "You have logged in", 'user_list': user_list})

            else:
                user_list = User.objects.filter(username=user.username)
                return render(request, 'ta.html', {
                    'message': "You have logged in", 'user_list': user_list})

        if user_obj is None:
            return render(request, 'login.html',
                          {'message': "There was an error logging you in, please try again"})


class adduser(View):
    def get(self, request):
        return render(request, "add_user.html", {'role_choices': Roles.choices})

    def post(self, request):
        new_user = AddUser(request.POST['username'], request.POST['password'], request.POST['fname'],
                           request.POST['lname'], request.POST['role'])
        isvalid = new_user.validate()
        check = new_user.checkUser()

        if isvalid and not check:
            User.objects.create(username=new_user.username, password=new_user.password, fname=new_user.fname,
                                lname=new_user.lname, role=new_user.role)
            return render(request, 'supervisor.html', {'message': "You have successfully added " + new_user.username})
        if check:
            return render(request, "add_user.html", {'message': "User already exists", 'role_choices': Roles.choices})
        if not isvalid:
            return render(request, "add_user.html", {'message': "There was an error validating the form",
                                                     'role_choices': Roles.choices})


class supervisor(View):
    def get(self, request):
        return render(request, "supervisor.html", {})


class instructor(View):
    def get(self, request):
        return render(request, "instructor.html", {})


class ta(View):
    def get(self, request):
        return render(request, "supervisor.html", {})


class LogoutView(View):
    def get(self, request):
        session_keys = list(request.session.keys())
        for key in session_keys:
            del request.session[key]
        return HttpResponseRedirect('/')  # Redirect to the homepage or login page
