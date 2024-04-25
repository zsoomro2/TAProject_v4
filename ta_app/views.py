from django.shortcuts import render, redirect
from django.views import View
from .models import User, Roles, Course
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
                user = User.objects.get(username=user.username)
                user_list = User.objects.all()
                course_list = Course.objects.all()
                return render(request, 'supervisor.html',
                              {'message': "You have logged in", 'user': user, 'user_list': user_list,
                               'course_list': course_list})

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
        users = User.objects.all()  # Fetch all user objects
        return render(request, "add_user.html", {'role_choices': Roles.choices, 'users': users})

    def post(self, request):
        new_user = AddUser(request.POST['username'], request.POST['password'], request.POST['fname'],
                           request.POST['lname'], request.POST['role'])
        isvalid = new_user.validate()
        check = new_user.checkUser()

        # Initialize the context with role_choices to always include them in the rendering
        context = {'role_choices': Roles.choices}

        if isvalid and not check:
            User.objects.create(username=new_user.username, password=new_user.password, fname=new_user.fname,
                                lname=new_user.lname, role=new_user.role)
            context['message'] = "You have successfully added " + new_user.username
        elif check:
            context['message'] = "User already exists"
        elif not isvalid:
            context['message'] = "There was an error validating the form"

        # Fetch all users regardless of the outcome to display the list of users
        context['users'] = User.objects.all()

        return render(request, "add_user.html", context)


class supervisor(View):
    def get(self, request):

        user_list = User.objects.all()
        course_list = Course.objects.all()
        return render(request, 'supervisor.html',{'user_list': user_list, 'course_list': course_list})


class instructor(View):
    def get(self, request):
        users = User.objects.all()  # Fetch all user objects
        return render(request, "instructor.html", {'users': users})


class ta(View):
    def get(self, request):
        return render(request, "supervisor.html", {})


class LogoutView(View):
    def get(self, request):
        session_keys = list(request.session.keys())
        for key in session_keys:
            del request.session[key]
        return HttpResponseRedirect('/')  # Redirect to the homepage or login page

class edit(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        return render(request, 'edit.html', {'username': user, 'role_choices': Roles.choices})
