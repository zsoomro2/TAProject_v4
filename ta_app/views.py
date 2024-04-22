from django.shortcuts import render, redirect
from django.views import View
from .models import User
from classes.Login import Login
# Create your views here.

class login(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        user = Login(request.POST['username'], request.POST['password'])
        user_obj = user.findUser(user.username, user.password)

        #create user_obj to grab a user/None type
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

class supervisor(View):
    def get(self, request):
        return render(request, "supervisor.html", {})

class instructor(View):
    def get(self, request):
        return render(request, "supervisor.html", {})

class ta(View):
    def get(self, request):
        return render(request, "supervisor.html", {})