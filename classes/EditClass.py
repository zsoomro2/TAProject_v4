from ta_app.models import User, Course
from django.shortcuts import get_object_or_404


class EditClass:
    def __init__(self, request, username):
        self.request = request
        self.username = username

    def isUser(self):
        return User.objects.filter(username=self.username).exists()

    def isCourse(self):
        return Course.objects.filter(Course_name=self.username).exists()

    def validateUsername(self, request, username):
        update_username = request.POST['username']
        user_list = User.objects.all()
        for user in user_list:
            if user.username == username:
                continue
            elif update_username == user.username:
                return False

        char_list = list(update_username)
        for char in char_list:
            if char == '@':
                return True
        return False


    def updateUser(self, request, username):
        validated = self.validateUsername(request, username)

        if validated:
            try:
                user = User.objects.get(username=username)
                user.username = request.POST.get('username', user.username)
                user.fname = request.POST.get('fname', user.fname)
                user.lname = request.POST.get('lname', user.lname)
                user.role = request.POST.get('role', user.role)

                # Preserve existing skills if not explicitly changed
                user.java_skill = 'java_skill' in request.POST or user.java_skill
                user.python_skill = 'python_skill' in request.POST or user.python_skill
                user.frontend_skill = 'frontend_skill' in request.POST or user.frontend_skill
                user.backend_skill = 'backend_skill' in request.POST or user.backend_skill
                user.scala_skill = 'scala_skill' in request.POST or user.scala_skill
                user.discrete_math_skill = 'discrete_math_skill' in request.POST or user.discrete_math_skill

                user.save()
                print(f"Updated user: {user.username}")
                return True
            except Exception as e:
                print(f"Update failed for user {username}: {e}")
                return False
        else:
            return False


    def updateCourse(self, thing):
        updated_course = [self.request.POST['CourseName'], self.request.POST['MeetType'],
                          self.request.POST['course_desc']]
        course_list = Course.objects.all()

        for course in course_list:
            if course.Course_name == thing:
                continue
            elif self.request.POST['CourseName'] == course.Course_name:
                return False

        update_course = get_object_or_404(Course, Course_name=thing)
        update_course.Course_name = updated_course[0]
        update_course.MeetType = updated_course[1]
        update_course.Course_description = updated_course[2]
        update_course.save()

        return True

