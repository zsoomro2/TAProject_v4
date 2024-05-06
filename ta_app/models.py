from django.db import models

# Create your models here.


# For html refrencing of classes, example: User.username = username
# For html refernence of linked tables: Courses.ta.username = username

# creating choices for role
class Roles(models.TextChoices):
    TA = "TA"
    Instructor = "Instructor"
    Supervisor = "Supervisor"

class MeetType(models.TextChoices):
    Online = "Online"
    InPerson = "In Person"
    Hybird = "Hybird"

class LecLab(models.TextChoices):
    Lecture = "Lecture"
    Lab = "Lab"


# creating User class for database
class User(models.Model):
    username = models.EmailField()
    password = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=Roles.choices)

    def __str__(self):
        return self.username


# creating Course class for database
# DATETIME FIELD EXAMPLE: 4/25/2024 12:00 AM
class Course(models.Model):
    Course_name = models.CharField(max_length=100)
    Course_description = models.TextField(max_length=1000, null=True, blank=True)
    MeetType = models.CharField(max_length=20, choices=MeetType.choices, default=MeetType.InPerson)
    # section = models.ManyToManyField("Section")

    def __str__(self):
        return self.Course_name

class Section(models.Model):
    Course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name="course")
    section_number = models.IntegerField()
    LecLab = models.CharField(max_length=20, choices=LecLab.choices, default=LecLab.Lecture)
    start = models.DateTimeField(max_length=20)
    end = models.DateTimeField(max_length=20)
    credits = models.IntegerField()
    instructor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="instructor")
    ta = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="ta")

    def __str__(self):
        return str(self.section_number)

