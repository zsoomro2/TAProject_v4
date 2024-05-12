from ta_app.models import User, Course


class EditClass:
    def __init__(self, request, username):
        self.request = request
        self.username = username

    def isUser(self):
        return User.objects.filter(username=self.username).exists()

    def isCourse(self):
        return Course.objects.filter(Course_name=self.username).exists()

    def updateUser(self, request, username):
        try:
            user = User.objects.get(username=username)
            print(f"Updating user {username}...")

            # Update user details
            user.fname = request.POST.get('fname')
            print(f"Updated fname: {user.fname}")

            user.lname = request.POST.get('lname')
            print(f"Updated lname: {user.lname}")

            user.role = request.POST.get('role')
            print(f"Updated role: {user.role}")

            # Update password if provided
            password = request.POST.get('password')
            if password:
                user.password = password
                print(f"Updated password for {username}")

            # Update skills
            user.java_skill = 'java_skill' in request.POST
            print(f"Updated java_skill: {user.java_skill}")

            user.python_skill = 'python_skill' in request.POST
            print(f"Updated python_skill: {user.python_skill}")

            user.frontend_skill = 'frontend_skill' in request.POST
            print(f"Updated frontend_skill: {user.frontend_skill}")

            user.backend_skill = 'backend_skill' in request.POST
            print(f"Updated backend_skill: {user.backend_skill}")

            user.scala_skill = 'scala_skill' in request.POST
            print(f"Updated scala_skill: {user.scala_skill}")

            user.discrete_math_skill = 'discrete_math_skill' in request.POST
            print(f"Updated discrete_math_skill: {user.discrete_math_skill}")

            # Save user
            user.save()
            print(f"User {username} updated successfully.")
            return True
        except Exception as e:
            print(f"Update failed for user {username}: {e}")
            return False


    def updateCourse(self, request, thing):

        updated_course = [request.POST['CourseName'], request.POST['MeetType'], request.POST['course_desc']]

        course_list = Course.objects.all()

        for course in course_list:

            if course.Course_name == thing:

                continue

            elif request.POST['CourseName'] == course.Course_name:

                return False

            else:

                update_course = Course.objects.get(Course_name=thing)

                update_course.Course_name = updated_course[0]

                update_course.MeetType = updated_course[1]

                update_course.Course_description = updated_course[2]

                update_course.save()

        return True


