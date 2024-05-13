from django.shortcuts import render, redirect
from django.views import View
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
        request.session.flush()
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
            request.session.set_expiry(1000)
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
            user = User.objects.create(username=new_user.username, password=new_user.password, fname=new_user.fname,
                                       lname=new_user.lname, role=new_user.role)
            user.java_skill = 'java_skill' in request.POST
            user.python_skill = 'python_skill' in request.POST
            user.frontend_skill = 'frontend_skill' in request.POST
            user.backend_skill = 'backend_skill' in request.POST
            user.scala_skill = 'scala_skill' in request.POST
            user.discrete_math_skill = 'discrete_math_skill' in request.POST
            user.save()
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
            return render(request, 'supervisor.html', {
                'user_list': user_list,
                'course_list': course_list,
                'section_list': section_list,
                'current_user': current_user
            })
        else:
            return render(request, 'login.html', {'message': 'Please login to view this page'})


class user_page(View):
    def get(self, request):
        if request.session.get('role') != 'Supervisor':
            return redirect_to_role_home(request)
        user_list = User.objects.all()
        return render(request, 'editUser.html', {'user_list': user_list})



class ta(View):
    def get(self, request):
        if request.session.get('role') != 'TA':
            return redirect_to_role_home(request)
        try:
            ta_user = User.objects.get(id=request.session['user_id'])
            sections_as_ta = Section.objects.filter(ta=ta_user)
            sections_as_instructor = Section.objects.filter(instructor=ta_user)
            sections = sections_as_ta.union(sections_as_instructor)  # Combine both querysets

            return render(request, "ta.html", {
                'ta': ta_user,
                'sections': sections
            })
        except User.DoesNotExist:
            return redirect('login')


class LogoutView(View):
    def get(self, request):
        session_keys = list(request.session.keys())
        for key in session_keys:
            del request.session[key]
        return HttpResponseRedirect('/')


class edit(View):
    def get(self, request, username):
        thing = EditClass(request, username)
        context = {'role_choices': Roles.choices}

        if thing.isUser():
            user = User.objects.get(username=username)
            if request.session.get('role') not in ['Supervisor', 'TA']:
                return redirect_to_role_home(request)

            context.update({
                'username': user,
                'isUser': thing.isUser(),
                'show_skills': request.session.get('role') != 'TA'  # Only show skills for non-TA
            })
            return render(request, 'edit.html', context)

        elif thing.isCourse():
            if request.session.get('role') != 'Supervisor':
                return redirect_to_role_home(request)

            course = Course.objects.get(Course_name=username)
            context.update({
                'username': course,
                'isCourse': thing.isCourse(),
                'MeetType': MeetType.choices
            })
            return render(request, 'edit.html', context)

    def post(self, request, username):
        thing = EditClass(request, username)
        isUser = thing.isUser()
        isCourse = thing.isCourse()
        update = False

        if isUser:
            if request.session.get('role') not in ['Supervisor', 'TA']:
                return redirect_to_role_home(request)

            update = thing.updateUser(request, username)

        elif isCourse:
            if request.session.get('role') != 'Supervisor':
                return redirect_to_role_home(request)

            update = thing.updateCourse(request, username)

        if update:
            # Redirect based on role
            if request.session.get('role') == 'TA':
                return redirect('ta')  # Redirect to TA homepage
            else:
                return redirect('supervisor')  # Redirect to Supervisor homepage

        else:
            context = {}
            if isUser:
                user = User.objects.get(username=username)
                context.update({
                    'username': user,
                    'role_choices': Roles.choices,
                    'message': "Error when updating user"
                })
            elif isCourse:
                course = Course.objects.get(Course_name=username)
                ta_list = User.objects.filter(role='TA')
                instructor_list = User.objects.filter(role='Instructor')
                context.update({
                    'username': course,
                    'ta_list': ta_list,
                    'instructor_list': instructor_list,
                    'isCourse': thing.isCourse(),
                    'message': "There was an error updating the course"
                })

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
        if request.session.get('role') != 'Supervisor':
            return redirect_to_role_home(request)
        return render(request, "addCourse.html", {'MeetType': MeetType})

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
        course = Course.objects.get(Course_name=course_name)

        # Define instructor_list and ta_list
        instructor_list = User.objects.filter(role="Instructor")
        ta_list = User.objects.filter(role="TA").distinct()

        # Format instructor and TA lists
        formatted_instructor_list = [
            f"{user.username} ({user.fname} {user.lname})"
            for user in instructor_list
        ]

        formatted_ta_list = [
            f"{user.username} ({user.fname} {user.lname} - Skills: {', '.join([skill for skill in ['Java', 'Python', 'Frontend', 'Backend', 'Scala', 'Discrete Math'] if getattr(user, f'{skill.lower().replace(' ', '_')}_skill')]) or 'No Skills Added'})"
            for user in ta_list
        ]

        if current_user and current_user.role == "Supervisor":
            return render(request, "addSection.html", {
                "course_data": course_data,
                "name": course_name,
                "LecLab": LecLab,
                "instructor_list": formatted_instructor_list,
                "ta_list": formatted_ta_list
            })
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

        instructor_str = request.POST.get("instructor", "")
        ta_str = request.POST.get("ta", "")

        # Extract username from formatted strings
        instructor_username = instructor_str.split(' ')[0] if instructor_str else None
        ta_username = ta_str.split(' ')[0] if ta_str else None

        instructor = None
        if instructor_username:
            try:
                instructor = User.objects.get(username=instructor_username)
            except User.DoesNotExist:
                instructor = None

        ta = None
        if ta_username:
            try:
                ta = User.objects.get(username=ta_username)
            except User.DoesNotExist:
                ta = None

        course_obj = Course.objects.get(Course_name=course)
        section_list = Section.objects.filter(Course=course_obj.id)

        # Define instructor_list and ta_list again
        instructor_list = User.objects.filter(role="Instructor")
        ta_list = User.objects.filter(role="TA").distinct()

        # Format instructor and TA lists
        formatted_instructor_list = [
            f"{user.username} ({user.fname} {user.lname})"
            for user in instructor_list
        ]

        formatted_ta_list = [
            f"{user.username} ({user.fname} {user.lname} - Skills: {', '.join([skill for skill in ['Java', 'Python', 'Frontend', 'Backend', 'Scala', 'Discrete Math'] if getattr(user, f'{skill.lower().replace(' ', '_')}_skill')]) or 'No Skills Added'})"
            for user in ta_list
        ]

        for section in section_list:
            if str(request.POST["sec_num"]) == str(section.section_number):
                context['message'] = "A section with this number already exists"
                context['course_data'] = Course.objects.filter(Course_name=course)
                context['name'] = course_name
                context['LecLab'] = LecLab
                context['instructor_list'] = formatted_instructor_list
                context['ta_list'] = formatted_ta_list
                return render(request, "addSection.html", context)
            if start_date > end_date or (start_date == end_date and start_time > end_time):
                context['message'] = "Cannot have start date/time after end"
                context['course_data'] = Course.objects.filter(Course_name=course)
                context['name'] = course_name
                context['LecLab'] = LecLab
                context['instructor_list'] = formatted_instructor_list
                context['ta_list'] = formatted_ta_list
                return render(request, "addSection.html", context)

        new_section = Section.objects.create(
            Course=course_obj,
            section_number=sec_num,
            LecLab=LecLab_obj,
            start=start,
            end=end,
            credits=credits,
            instructor=instructor,
            ta=ta
        )
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
        ta_list = User.objects.filter(role="TA").distinct()
        instructor_list = User.objects.filter(role="Instructor")

        section = Section.objects.get(section_number=section_number)
        start = section.start
        end = section.end

        context = {
            "section": section,
            "name": course_name,
            "ta_list": ta_list,
            "instructor_list": instructor_list,
            "LecLab": LecLab,
            "start_date": start.strftime("%Y-%m-%dT%H:%M"),
            "end_date": end.strftime("%Y-%m-%dT%H:%M")
        }
        return render(request, "updatesection.html", context)

    def post(self, request, course_name, section_number):
        section = Section.objects.get(section_number=section_number)
        section.LecLab = request.POST["LecLab"]
        section.start = datetime.strptime(request.POST["start"], "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)
        section.end = datetime.strptime(request.POST["end"], "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)
        section.credits = request.POST["credits"]

        instructor_str = request.POST.get("instructor", "")
        ta_str = request.POST.get("ta", "")

        instructor_username = instructor_str.split(' ')[0] if instructor_str else None
        ta_username = ta_str.split(' ')[0] if ta_str else None

        if instructor_username:
            try:
                section.instructor = User.objects.get(username=instructor_username)
            except User.DoesNotExist:
                section.instructor = None

        if ta_username:
            try:
                section.ta = User.objects.get(username=ta_username)
            except User.DoesNotExist:
                section.ta = None

        section.save()
        return redirect('supervisor')


class edit_ta_skills(View):
    def get(self, request):
        if request.session.get('role') != 'TA':
            return redirect_to_role_home(request)
        try:
            ta = User.objects.get(id=request.session['user_id'])
            return render(request, 'edit_ta_skills.html', {'ta': ta})
        except User.DoesNotExist:
            return redirect('login')

    def post(self, request):
        if request.session.get('role') != 'TA':
            return redirect_to_role_home(request)
        try:
            ta = User.objects.get(id=request.session['user_id'])
            ta.java_skill = 'java_skill' in request.POST
            ta.python_skill = 'python_skill' in request.POST
            ta.frontend_skill = 'frontend_skill' in request.POST
            ta.backend_skill = 'backend_skill' in request.POST
            ta.scala_skill = 'scala_skill' in request.POST
            ta.discrete_math_skill = 'discrete_math_skill' in request.POST
            ta.save()
            return redirect('ta')
        except User.DoesNotExist:
            return redirect('login')


class instructor(View):
    def get(self, request):
        if request.session.get('role') != 'Instructor':
            return redirect_to_role_home(request)
        try:
            instructor_user = User.objects.get(id=request.session['user_id'])
            sections = Section.objects.filter(instructor=instructor_user)
            available_tas = User.objects.filter(role='TA')  # Assuming TA role is identified by 'TA'

            return render(request, "instructor.html", {
                'instructor': instructor_user,
                'sections': sections,
                'tas': available_tas
            })
        except User.DoesNotExist:
            return redirect('login')

    def post(self, request, section_id):
        try:
            section = Section.objects.get(id=section_id)
        except Section.DoesNotExist:
            section = None

        if section:
            ta_id = request.POST.get('ta_id')
            try:
                if ta_id:
                    ta_user = User.objects.get(id=ta_id)
                    section.ta = ta_user
                    section.save()
            except User.DoesNotExist:
                pass  # Handle error if TA does not exist

        return redirect('instructor')



class AddTA(View):
    def post(self, request, section_id):
        try:
            section = Section.objects.get(id=section_id)
            ta_id = request.POST.get('ta_id')
            if ta_id:
                try:
                    ta_user = User.objects.get(id=ta_id)
                    section.ta = ta_user
                    section.save()
                    return redirect('instructor')
                except User.DoesNotExist:
                    return render(request, 'instructor.html', {
                        'error': 'TA does not exist.',
                        'sections': Section.objects.all(),
                        'tas': User.objects.filter(role='TA')
                    })
        except Section.DoesNotExist:
            return render(request, 'instructor.html', {
                'error': 'Section does not exist.',
                'sections': Section.objects.all(),
                'tas': User.objects.filter(role='TA')
            })


class RemoveTA(View):
    def get(self, request, section_id):
        try:
            section = Section.objects.get(id=section_id)
            section.ta = None
            section.save()
        except Section.DoesNotExist:
            return redirect('instructor')
        return redirect('instructor')