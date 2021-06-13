"""School URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from gms_admin import studentViews, teacherViews, views, adminViews
from School import settings

urlpatterns = [

    #ADMIN
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('',views.loginPage, name='show_login'),
    path('dashboard/', views.adminHome, name='admin_home'),
    path('get_user ',views.GetUser),
    path('logout',views.logout_user, name='logout'),
    path('doLogin', views.doLogin, name='do_login'),
    path('admin_home',adminViews.admin_home),
    path('add_teacher', adminViews.add_teacher, name='add_teacher'),
    path('save_teacher', adminViews.save_teacher, name='save_teacher'),
    path('add_gradelevel', adminViews.add_gradelevel, name='add_gradelevel'),
    path('save_gradelevel', adminViews.save_gradelevel, name='save_gradelevel'),
    path('add_student', adminViews.add_student, name='add_student'),
    path('save_student', adminViews.save_student, name='save_student'),
    path('add_subjects', adminViews.add_subjects, name='add_subjects'),
    path('save_subjects', adminViews.save_subjects, name='save_subjects'),
    path('sections', adminViews.sections, name='view_section'),
    path('get_section', adminViews.get_section, name='get_section'  ),
    path('add_class', adminViews.add_class, name='add_class'),
    path('save_class', adminViews.save_class, name='save_class'),
    path('edit_teacher/<str:teacher_id>', adminViews.edit_teacher),
    path('save_editteacher', adminViews.save_editteacher, name="save_editteacher"),
    path('edit_student/<str:student_id>', adminViews.edit_student, name='edit_student'),
    path('save_editstudent', adminViews.save_editstudent, name='save_editstudent'),
    path('edit_subject/<str:subject_id>', adminViews.edit_subject, name="edit_subject"),
    path('save_editsubject', adminViews.save_editsubject, name='save_editsubject'),
    path('edit_class/<str:class_id>', adminViews.edit_class, name='edit_class'),
    path('save_editclass', adminViews.save_editclass, name="save_editclass"),
    path('delete_gradelevel/<str:gradelevel_id>', adminViews.delete_gradelevel),
    path('manage_student', adminViews.manage_student, name='manage_student'),
    path('manage_teacher', adminViews.manage_teacher, name='manage_teacher'),
    path('manage_subject', adminViews.manage_subject, name='manage_subject'),
    path('manage_school', adminViews.manage_school, name='manage_school'),
    path('add_sessionyear', adminViews.add_sessionyear, name='add_sessionyear'), 
    path('save_sessionyear', adminViews.save_sessionyear, name='save_sessionyear'),
    path('add_sectionsubjects/<str:student_id>', adminViews.add_sectionsubjects, name='add_sectionsubjects'), 
    path('save_sectionsubjects', adminViews.save_sectionsubjects, name='save_sectionsubjects'),


    #TEACHER

    path('teacher_home', teacherViews.teacher_home, name='teacher_home'),
    path('view_subjects', teacherViews.view_subjects, name='view_subjects'),
    path('attendance', teacherViews.attendance, name='attendance'),
    path('get_students', teacherViews.get_students, name="get_students"),
    path('save_attendance', teacherViews.save_attendance, name="save_attendance"),
    path('update_attendance', teacherViews.update_attendance, name="update_attendance"),
    path('get_attendance', teacherViews.get_attendance, name="get_attendance"),
    path('get_attendance_students', teacherViews.get_attendance_students, name="get_attendance_students"),
    path('save_update_attendance', teacherViews.save_update_attendance, name="save_update_attendance"), 
    path('grade', teacherViews.grade, name="grade"),
    path('get_subject_students', teacherViews.get_subject_students, name="get_subject_students"),


    #STUDENT

    path('student_home', studentViews.student_home, name='student_home'),
    path('student_subjects', studentViews.student_subjects, name='student_subjects'),
    path('view_attendance', studentViews.view_attendance, name='view_attendance')



    #PARENT


]
