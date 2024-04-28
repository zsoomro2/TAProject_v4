from ta_app.models import User, Course, Roles
from .AddUser import AddUser

class EditClass():
    def __init__(self, request, thing):
        self.thing = thing

    def isUser(self):
        user_list = User.objects.all()
        for user in user_list:
            if user.username == self.thing:
                return True
        return False

    def updateUser(self, request, thing):
        updated_user = AddUser(request.POST['username'], request.POST['password'], request.POST['fname'], request.POST['lname'],
                       request.POST['role'])
        validate = updated_user.validate()
        user_list = User.objects.all()
        for user in user_list:
            if user.username == thing:
                continue
            elif updated_user.username == user.username or not validate:
                return False
            else:
                update_user = User.objects.get(username=thing)
                update_user.username = request.POST['username']
                update_user.password = request.POST['password']
                update_user.fname = request.POST['fname']
                update_user.lname = request.POST['lname']
                update_user.role = request.POST['role']
                update_user.save()
        return True

    def isCourse(self):
        course_list = Course.objects.all()
        for course in course_list:
            if course.Course_name == self.thing:
                return True
        return False

    def updateCourse(self, request, thing):
        updated_course = [request.POST['CourseName'], request.POST['section'], request.POST['start'], request.POST['end']
                          , request.POST['credits'], request.POST['instructor'], request.POST['ta']]

        for data in updated_course:
            if data == "" or data is None:
                return False

        update_course = Course.objects.get(Course_name=thing)
        update_course.Course_name = updated_course[0]
        update_course.Section = updated_course[1]
        update_course.Start = updated_course[2]
        update_course.End = updated_course[3]
        update_course.credits = updated_course[4]
        instructor = User.objects.get(username=request.POST['instructor'])
        update_course.instructor = instructor
        ta = User.objects.get(username=request.POST['ta'])
        update_course.ta = ta
        update_course.save()
        return True