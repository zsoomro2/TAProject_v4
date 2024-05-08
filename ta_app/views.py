from django.shortcuts import render, redirect
from django.views import View
from .models import User, Roles, Course, Section, MeetType
from classes.Login import Login
from classes.AddUser import AddUser
from classes.EditClass import EditClass
from classes.User import MyUser
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
                section_list = Section.objects.all()
                return render(request, 'supervisor.html',
                              {'message': "You have logged in", 'user': user, 'user_list': user_list,
                               'course_list': course_list, 'section_list': section_list})


            elif user.getRole() == "Instructor":
                user = User.objects.get(username=user.username)
                return render(request, 'instructor.html',
                              {'message': "You have logged in", 'user': user.username})

            else:
                user = User.objects.get(username=user.username)
                return render(request, 'ta.html', {
                    'message': "You have logged in", 'user': user.username})
        request.session.set_expiry(300)

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
        context['user_list'] = User.objects.all()
        context['course_list'] = Course.objects.all()
        context['section_list'] = Section.objects.all()
        return render(request, "supervisor.html", context)


class supervisor(View):
    def get(self, request):
        user_list = User.objects.all()
        course_list = Course.objects.all()
        section_list = Section.objects.all()
        return render(request, 'supervisor.html', {'user_list': user_list, 'course_list': course_list
            , 'section_list': section_list})


class user_page(View):
    def get(self, request):
        user_list = User.objects.all()
        return render(request, 'editUser.html', {'user_list': user_list})


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
        thing = EditClass(request, username)
        if thing.isUser():
            user = User.objects.get(username=username)
            return render(request, 'edit.html', {'username': user, 'role_choices': Roles.choices,
                                                 'isUser': thing.isUser()})

        elif thing.isCourse():
            course = Course.objects.get(Course_name=username)
            # ta_list = User.objects.filter(role='TA')
            # instructor_list = User.objects.filter(role='Instructor')
            context = {'username': course, 'isCourse': thing.isCourse(), 'MeetType': MeetType.choices}
            return render(request, 'edit.html', context)

    def post(self, request, username):
        thing = EditClass(request, username)
        isUser = thing.isUser()
        isCourse = thing.isCourse()
        user_list = User.objects.all()
        course_list = Course.objects.all()
        section_list = Section.objects.all()
        context = {}

        if isUser:
            update = thing.updateUser(request, username)

        elif isCourse:
            update = thing.updateCourse(request, username)

        if update:
            context = {'user_list': user_list, 'course_list': course_list, 'section_list': section_list,
                       'message': "You have edited " + username}
            return render(request, 'supervisor.html', context)

        else:
            if isUser:
                user = User.objects.get(username=username)
                context = {'username': user, 'role_choices': Roles.choices, 'message': "Error when updating user"}

            elif isCourse:
                course = Course.objects.get(Course_name=username)
                ta_list = User.objects.filter(role='TA')
                instructor_list = User.objects.filter(role='Instructor')
                context = {'username': course, 'ta_list': ta_list, 'instructor_list': instructor_list,
                           'isCourse': thing.isCourse(), 'message': "There was an error updating the course"}

        return render(request, 'edit.html', context)


class Delete(View):
    def get(self, request, username):
        return render(request, 'delete.html', {'username': username})

    def post(self, request, username):
        thing = EditClass(request, username)
        if thing.isUser():
            user = User.objects.get(username=username)
            user.delete()

        elif thing.isCourse():
            course = Course.objects.get(Course_name=username)
            sections = Section.objects.filter(Course=course)
            for section in sections:
                section.delete()
            course.delete()

        user_list = User.objects.all()
        course_list = Course.objects.all()
        section_list = Section.objects.all()
        return render(request, 'supervisor.html', {'user_list': user_list,
                                                   'course_list': course_list,
                                                   'message': "You have deleted " + username,
                                                   'section_list': section_list})


class ViewCourse(View):
    def get(self, request, course_name):
        course = Course.objects.filter(Course_name=course_name)
        section_list = Section.objects.all()
        return render(request, 'viewcourse.html', {'course_list': course,
                                                   'section_list': section_list, 'course_name': course_name})


class viewAssignments(View):
    def get(self, request):
        users = User.objects.all()
        assignments = []

        for user in users:
            sections_as_ta = Section.objects.filter(ta=user)
            sections_as_instructor = Section.objects.filter(instructor=user)

            if not sections_as_ta.exists() and not sections_as_instructor.exists():
                assignments.append({
                    'user': f"{user.fname} {user.lname}",
                    'sections': 'No current assignments'
                })
            else:
                all_sections = sections_as_ta | sections_as_instructor
                for section in all_sections:
                    assignments.append({
                        'user': f"{user.fname} {user.lname}",
                        'course_name': section.Course.Course_name,
                        'section_number': section.section_number,
                        'instructor': f"{section.instructor.fname} {section.instructor.lname}" if section.instructor else "No instructor",
                        'ta': f"{section.ta.fname} {section.ta.lname}" if section.ta else "No TA"
                    })

        return render(request, "viewAssignments.html", {'assignments': assignments})
