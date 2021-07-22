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
from gms_admin import studentViews, teacherViews, adminViews, views
from School import settings
import gms_admin

urlpatterns = [

    #ADMIN
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('',views.otp_view, name='otp_view'),
    path('login',views.loginPage, name='show_login'),
    path('send_otp',views.send_otp, name='send_otp'),
    path('verify_otp',views.verify_otp, name='verify_otp'),
    path('confirm_otp',views.confirm_otp, name='confirm_otp'),
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
    path('edit_gradelevel/<str:gradelevel_id>',adminViews.edit_gradelevel, name='edit_gradelevel'),
    path('save_editgradelevel',adminViews.save_editgradelevel, name='save_editgradelevel'),
    path('delete_gradelevel/<str:gradelevel_id>', adminViews.delete_gradelevel),
    path('delete_class/<str:class_id>', adminViews.delete_class),
    path('delete_year/<str:schoolyear_id>', adminViews.delete_year),
    path('delete_subject/<str:subject_id>', adminViews.delete_subject),
    path('delete_student/<str:student_id>', adminViews.delete_student),
    path('delete_teacher/<str:teacher_id>', adminViews.delete_teacher),
    path('manage_student', adminViews.manage_student, name='manage_student'),
    path('manage_teacher', adminViews.manage_teacher, name='manage_teacher'),
    path('manage_subject', adminViews.manage_subject, name='manage_subject'),
    path('manage_school', adminViews.manage_school, name='manage_school'),
    path('add_sessionyear', adminViews.add_sessionyear, name='add_sessionyear'), 
    path('save_sessionyear', adminViews.save_sessionyear, name='save_sessionyear'),
    path('add_sectionsubjects/<str:student_id>', adminViews.add_sectionsubjects, name='add_sectionsubjects'), 
    path('save_sectionsubjects', adminViews.save_sectionsubjects, name='save_sectionsubjects'),
    path('djrichtextfield/', include('djrichtextfield.urls')),
    path('admin_chat', adminViews.admin_chat, name='admin_chat'),
    path('admin_send_message', adminViews.adminsend_message, name='admin_send_message'),
    
    
    #TEACHER
    path('send_message', teacherViews.send_message, name='send_message'),

    path('teacher_home', teacherViews.teacher_home, name='teacher_home'),
    path('view_subjects', teacherViews.view_subjects, name='view_subjects'),

    path('view_grades/<str:subject_id>', teacherViews.view_grades, name='view_grades'),
    path('attendance', teacherViews.attendance, name='attendance'),
    path('get_students', teacherViews.get_students, name="get_students"),
    path('save_attendance', teacherViews.save_attendance, name="save_attendance"),
    path('update_attendance', teacherViews.update_attendance, name="update_attendance"),
    path('get_attendance', teacherViews.get_attendance, name="get_attendance"),
    path('get_attendance_students', teacherViews.get_attendance_students, name="get_attendance_students"),
    path('save_update_attendance', teacherViews.save_update_attendance, name="save_update_attendance"), 
    path('grade', teacherViews.grade, name="grade"),
    path('get_subject_students', teacherViews.get_subject_students, name="get_subject_students"),
    path('add_activity/<str:section_subject_id>', teacherViews.add_activity, name ="add_activity"),
    path('add_quiz', teacherViews.add_quiz, name='add_quiz'),
    path('get_sectionsubject', teacherViews.get_sectionsubject, name='get_sectionsubject'),
    path('announcement', teacherViews.announcement, name='announcement'),
    path('edit_announcement/<str:announcement_id>', teacherViews.edit_announcement, name='edit_announcement'),
    path('save_announcement', teacherViews.save_announcement, name='save_announcement'),
    path('save_editannouncement', teacherViews.save_editannouncement, name='save_editannouncement'),

    path('add_homework', teacherViews.add_homework, name='add_homework'),
    path('add_seatwork', teacherViews.add_seatwork, name='add_seatwork'),
    path('add_exam', teacherViews.add_exam, name='add_exam'),
    path('add_performance', teacherViews.add_performance, name='add_performance'),


    path('get_homework', teacherViews.get_homework, name='get_homework'),
    path('get_quiz', teacherViews.get_quiz, name='get_quiz'),
    path('get_seatwork', teacherViews.get_seatwork, name='get_seatwork'),
    path('get_performance', teacherViews.get_performance, name='get_performance'),
    path('get_exam', teacherViews.get_exam, name='get_exam'),

    path('save_grade', teacherViews.save_grade, name='save_grade'),

    path('edit_homework/<str:homework_id>', teacherViews.edit_homework, name='edit_homework' ),
    path('edit_quiz/<str:quiz_id>', teacherViews.edit_quiz, name='edit_quiz' ),
    path('edit_seatwork/<str:seatwork_id>', teacherViews.edit_seatwork, name='edit_seatwork' ),
    path('edit_exam/<str:exam_id>', teacherViews.edit_exam, name='edit_exam' ),
    path('edit_performance/<str:performance_id>', teacherViews.edit_performance, name='edit_performance' ),

    path('save_edithomework', teacherViews.save_edithomework, name='save_edithomework'),
    path('save_editquiz', teacherViews.save_editquiz, name='save_editquiz'),
    path('save_editseatwork', teacherViews.save_editseatwork, name='save_editseatwork'),
    path('save_editexam', teacherViews.save_editexam, name='save_editexam'),
    path('save_editperformance', teacherViews.save_editperformance, name='save_editperformance'),
    path('chat', teacherViews.chat, name='chat'),
    #path('inbox/',include('gms_admin.urls')),
    #path("send_otp",views.send_otp,name="send otp"),
    #STUDENT

    path('student_home', studentViews.student_home, name='student_home'),
    path('student_subjects', studentViews.student_subjects, name='student_subjects'),
    path('view_attendance', studentViews.view_attendance, name='view_attendance'),
    path('view_announcement', studentViews.view_announcements, name='view_announcements'),
    path('view_grades', studentViews.view_grades, name='view_grades'),
    path('view_grades_details/<str:section_subject_id>', studentViews.view_grades_details, name='view_grades_details'),
    path('view_activities/<str:section_subject_id>', studentViews.view_activities, name='view_activities'),
    path('student_chat', studentViews.chat, name='student_chat'),
    path('student_send_message', studentViews.send_message, name='student_send_message'),



    #PARENT


]
