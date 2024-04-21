from django.db import models


# Create your models here.


# For html refrencing of classes, example: User.username = username
# For html refernence of linked tables: Courses.ta.username = username

# creating choices for role
class Roles(models.TextChoices):
    TA = "TA"
    Instructor = "Instructor"
    Supervisor = "Supervisor"


3


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
class Course(models.Model):
    Course_name = models.CharField(max_length=100)
    section = models.IntegerField()
    start = models.DateField(max_length=20)
    end = models.DateField(max_length=20)
    credits = models.IntegerField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="instructor")
    ta = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ta")

    def __str__(self):
        return str(self.section) + " " + self.Course_name
