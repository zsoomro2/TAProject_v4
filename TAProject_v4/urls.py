"""
URL configuration for TAProject_v4 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ta_app.views import (login, supervisor, instructor, ta,
                          adduser, LogoutView, edit, Delete, user_page, ViewCourse, viewAssignments, addCourse,
                          addSection, updateSection, edit_ta_skills, AddTA, RemoveTA, DeleteSection)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login.as_view(), name='login'),
    path('supervisor/', supervisor.as_view(), name='supervisor'),
    path('instructor/', instructor.as_view(), name='instructor'),
    path('add_ta/<int:section_id>/', AddTA.as_view(), name='add_ta'),
    path('remove_ta/<int:section_id>/', RemoveTA.as_view(), name='remove_ta'),
    path('ta/', ta.as_view(), name='ta'),
    path('adduser/', adduser.as_view(), name='adduser'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit.html/<str:username>', edit.as_view(), name='edit'),
    path('delete.html/<str:username>', Delete.as_view(), name='delete'),
    path('user_page.html/', user_page.as_view(), name='userpage'),
    path('view_page.html/<str:course_name>', ViewCourse.as_view(), name='viewcourse'),
    path('viewassignments/', viewAssignments.as_view(), name='viewassignments'),
    path('addcourse/', addCourse.as_view(), name='addcourse'),
    path('addsection/<str:course_name>', addSection.as_view(), name='addsection'),
    path('updatesection/<str:course_name>/<int:section_number>', updateSection.as_view(), name='updatesection'),
    path('edit_ta_skills/', edit_ta_skills.as_view(), name='edit_ta_skills'),
    path('deletesection/<str:course>/<int:section>/', DeleteSection.as_view(), name='deletesection')

]
