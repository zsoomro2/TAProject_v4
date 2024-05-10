from django.shortcuts import render, redirect
from django.views import View

from classes.InstructorClass import Instructor
from .models import User, Roles, Course, Section, MeetType, LecLab
from classes.Login import Login
from classes.AddUser import AddUser
from classes.EditClass import EditClass
from classes.User import MyUser
from django.http import HttpResponseRedirect
from datetime import datetime, timezone


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

        try:
            current_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            current_user = None


        if current_user and current_user.role == "Supervisor":
            return render(request, 'supervisor.html', {'user_list': user_list, 'course_list': course_list
                ,'section_list': section_list,'current_user': current_user})
        else:
            return render(request, 'login.html', {'message': 'Please login to view this page'})

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

class addCourse(View):
    def get(self, request):
        return render(request, "addCourse.html", {'MeetType':MeetType})

    def post(self, request):
        context = {}
        name = request.POST["CourseName"]
        meet = request.POST["MeetType"]
        desc = request.POST["coursedesc"]

        course_list = Course.objects.all()
        for course in course_list:
            if course.Course_name == name:
                context["message"] = "Course already exists"
                context["MeetType"] = MeetType
                return render(request, "addCourse.html", context)
        new_course = Course(Course_name=name, MeetType=meet, Course_description=desc)
        new_course.save()

        context["message"] = "You have successfully added " + name
        context["user_list"] = User.objects.all()
        context["course_list"] = Course.objects.all()
        context["section_list"] = Section.objects.all()
        return render(request, "supervisor.html", context)

class addSection(View):
    def get(self, request, course_name):
        user_id = request.session.get('user_id')
        try:
            current_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            current_user = None

        course_data = Course.objects.filter(Course_name=course_name)
        instructor_list = User.objects.filter(role="Instructor")
        ta_list = User.objects.filter(role="TA")
        if current_user and current_user.role == "Supervisor":
            return render(request, "addSection.html", {"course_data": course_data, "name":course_name,
                                            "LecLab":LecLab, "instructor_list": instructor_list, "ta_list": ta_list})
        else:
            return render(request, "login.html", {"message": "You have to login to view this page"})
    def post(self, request, course_name):
        context = {}
        course = course_name
        sec_num = request.POST["sec_num"]
        LecLab_obj = request.POST["LecLab"]
        start = request.POST["start"]
        end = request.POST["end"]
        credits = request.POST["credits"]
        start_date = datetime.strptime(start, "%Y-%m-%dT%H:%M").date()
        end_date = datetime.strptime(end, "%Y-%m-%dT%H:%M").date()
        start_time = datetime.strptime(start, "%Y-%m-%dT%H:%M").time()
        end_time = datetime.strptime(end, "%Y-%m-%dT%H:%M").time()

        instructor = request.POST["instructor"]
        if instructor != "":
            instructor = User.objects.get(username=instructor)
        else:
            instructor = None

        ta = request.POST["ta"]
        if ta != "":
            ta = User.objects.get(username=ta)
        else:
            ta = None

        course_obj = Course.objects.get(Course_name=course)
        section_list = Section.objects.filter(Course=course_obj.id)

        for section in section_list:
            if str(request.POST["sec_num"]) == str(section.section_number):
                context['message'] = "A section with this number already exists"
                context['course_data'] = Course.objects.filter(Course_name=course)
                context['name'] = course_name
                context['LecLab'] = LecLab
                context['instructor_list'] = User.objects.filter(role="Instructor")
                context['ta_list'] = User.objects.filter(role="TA")
                return render(request, "addSection.html", context)
            if start_date > end_date or (start_date == end_date and start_time > end_time):
                context['message'] = "Cannot have start date/time after end"
                context['course_data'] = Course.objects.filter(Course_name=course)
                context['name'] = course_name
                context['LecLab'] = LecLab
                context['instructor_list'] = User.objects.filter(role="Instructor")
                context['ta_list'] = User.objects.filter(role="TA")
                return render(request, "addSection.html", context)


        new_section = Section.objects.create(Course=course_obj, section_number=sec_num, LecLab=LecLab_obj, start=start, end=end,
                                             credits=credits, instructor=instructor, ta=ta)
        new_section.save()
        context['message'] = "You have added " + str(sec_num) + " to " + course_name
        context['user_list'] = User.objects.all()
        context['course_list'] = Course.objects.all()
        context['section_list'] = Section.objects.all()
        return render(request, "supervisor.html", context)

class updateSection(View):
    def get(self, request, course_name, section_number):

        course = Course.objects.get(Course_name=course_name)
        section_list = Section.objects.filter(Course=course.id)
        ta_list = User.objects.filter(role="TA")
        instructor_list = User.objects.filter(role="Instructor")

        section = None
        for item in section_list:
            if str(item.section_number) == str(section_number):
                section = Section.objects.get(section_number=section_number)
                start = section.start
                start.replace(tzinfo=None)
                end = section.end
                end.replace(tzinfo=None)
                start_date = datetime.strptime(str(start), "%Y-%m-%d %H:%M:%S%z")
                end_date = datetime.strptime(str(end), "%Y-%m-%d %H:%M:%S%z")
        return render(request, "updatesection.html", {"section": section, "name": course_name,
                    "ta_list": ta_list, "instructor_list":instructor_list, "LecLab":LecLab, "start_date":start_date, "end_date":end_date})
    def post(self, request, course_name, section_number):
        pass