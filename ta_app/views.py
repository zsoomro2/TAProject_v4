from django.shortcuts import render, redirect
from django.views import View
from .models import User, Roles, Course, Section, MeetType
from classes.Login import Login
from classes.AddUser import AddUser
from classes.EditClass import EditClass
from classes.User import MyUser
from django.http import HttpResponseRedirect


# Utility function to redirect based on role
def redirect_to_role_home(request):
    role = request.session.get('role', 'login').lower()
    return redirect(role)


class login(View):

    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = Login(username, password)
        user_obj = user.findUser(username, password)

        if user_obj is not None:
            request.session.flush()
            request.session['user_id'] = user_obj.id
            request.session['role'] = user_obj.role
            request.session.set_expiry(300)  # Session expires in 5 minutes
            request.session.modified = True

            return redirect_to_role_home(request)
        else:
            return render(request, 'login.html', {'message': "Login failed. Please try again."})


class adduser(View):
    def get(self, request):
        if request.session.get('role') != 'Supervisor':
            return redirect_to_role_home(request)
        users = User.objects.all()
        return render(request, "add_user.html", {'role_choices': Roles.choices, 'users': users})

    def post(self, request):
        if request.session.get('role') != 'Supervisor':
            return redirect_to_role_home(request)
        new_user = AddUser(request.POST['username'], request.POST['password'], request.POST['fname'],
                           request.POST['lname'], request.POST['role'])
        isvalid = new_user.validate()
        check = new_user.checkUser()

        context = {'role_choices': Roles.choices}

        if isvalid and not check:
            User.objects.create(username=new_user.username, password=new_user.password, fname=new_user.fname,
                                lname=new_user.lname, role=new_user.role)
            context['message'] = "You have successfully added " + new_user.username
        elif check:
            context['message'] = "User already exists"
        elif not isvalid:
            context['message'] = "There was an error validating the form"

        context['user_list'] = User.objects.all()
        context['course_list'] = Course.objects.all()
        context['section_list'] = Section.objects.all()
        return render(request, "supervisor.html", context)


class supervisor(View):
    def get(self, request):
        if request.session.get('role') != 'Supervisor':
            return redirect_to_role_home(request)
        user_list = User.objects.all()
        course_list = Course.objects.all()
        section_list = Section.objects.all()
        user_id = request.session.get('user_id')

        current_user = User.objects.get(id=user_id)
        return render(request, 'supervisor.html', {'user_list': user_list, 'course_list': course_list,
                                                   'section_list': section_list, 'current_user': current_user})


class user_page(View):
    def get(self, request):
        if request.session.get('role') != 'Supervisor':
            return redirect_to_role_home(request)
        user_list = User.objects.all()
        return render(request, 'editUser.html', {'user_list': user_list})


class instructor(View):
    def get(self, request):
        if request.session.get('role') != 'Instructor':
            return redirect_to_role_home(request)
        users = User.objects.all()
        return render(request, "instructor.html", {'users': users})


class ta(View):
    def get(self, request):
        if request.session.get('role') != 'TA':
            return redirect_to_role_home(request)
        return render(request, "ta.html", {})


class LogoutView(View):
    def get(self, request):
        session_keys = list(request.session.keys())
        for key in session_keys:
            del request.session[key]
        return HttpResponseRedirect('/')


class edit(View):
    def get(self, request, username):
        thing = EditClass(request, username)
        if thing.isUser():
            if request.session.get('role') != 'Supervisor':
                return redirect_to_role_home(request)
            user = User.objects.get(username=username)
            return render(request, 'edit.html', {'username': user, 'role_choices': Roles.choices,
                                                 'isUser': thing.isUser()})

        elif thing.isCourse():
            if request.session.get('role') != 'Supervisor':
                return redirect_to_role_home(request)
            course = Course.objects.get(Course_name=username)
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
            if request.session.get('role') != 'Supervisor':
                return redirect_to_role_home(request)
            update = thing.updateUser(request, username)

        elif isCourse:
            if request.session.get('role') != 'Supervisor':
                return redirect_to_role_home(request)
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
        if request.session.get('role') != 'Supervisor':
            return redirect_to_role_home(request)
        return render(request, 'delete.html', {'username': username})

    def post(self, request, username):
        if request.session.get('role') != 'Supervisor':
            return redirect_to_role_home(request)
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
        if request.session.get('role') not in ['Supervisor', 'Instructor']:
            return redirect_to_role_home(request)
        course = Course.objects.filter(Course_name=course_name)
        section_list = Section.objects.all()
        return render(request, 'viewcourse.html', {'course_list': course,
                                                   'section_list': section_list, 'course_name': course_name})


class viewAssignments(View):
    def get(self, request):
        if request.session.get('role') != 'Supervisor':
            return redirect_to_role_home(request)
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
