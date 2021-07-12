from django.contrib import admin
from gms_admin.models import*
from django.shortcuts import render


def student_home(request):
    return render(request, 'main/student_dashboard.html')


def view_section(request):
    pass

def student_subjects(request):
    current_user = request.user
    admin_id = current_user.id
    student = Students.objects.get(admin_id=admin_id)
    student_subjects = Section_subjects.objects.filter(student_id = admin_id)
    return render(request, 'student/subjects.html', {'subjects':student_subjects})


def view_attendance(request):
    current_user = request.user
    admin_id = current_user.id
    student = Students.objects.get(admin_id=admin_id)
    print(student)
    class_id = student.class_id
    attendance = Attendance.objects.filter(class_id=class_id)
    print(attendance)
    attendance_report = AttendanceReport.objects.filter(student_id = student)
    print(attendance_report)
    return render(request, 'student/view_attendance.html', {'attendance':attendance,'attendance_report':attendance_report})


def view_announcements(request):
    current_user = request.user
    admin_id = current_user.id
    student = Students.objects.values_list('class_id', flat=True).get(admin_id=admin_id)
    class_id = Classes.objects.get(id=student)
  
    subjects = Subjects.objects.filter(class_id=class_id)
    post = Announcements.objects.filter(subject_id__in=subjects)
    print(post)
    return render(request, 'student/view_announcements.html', {'post':post})


def view_grades(request):
    current_user = request.user
    admin_id = current_user.id
    student = Section_subjects.objects.filter(student_id = admin_id)
    student_subject = Section_subjects.objects.filter(student_id = admin_id)
    first_qtr = First_Qtr.objects.filter(section_subject_id__in = student)
    second_qtr = Second_Qtr.objects.filter(section_subject_id__in = student)
    third_qtr = Third_Qtr.objects.filter(section_subject_id__in = student)
    fourth_qtr = Fourth_Qtr.objects.filter(section_subject_id__in = student)
    print(first_qtr, second_qtr,third_qtr,fourth_qtr)
    return render(request, 'student/view_grades.html', {'student_subject':student_subject, 'first_qtr':first_qtr,'second_qtr':second_qtr,'third_qtr':third_qtr,'fourth_qtr':fourth_qtr})


def view_grades_details(request):
    current_user = request.user
    admin_id = current_user.id
    
    student = Section_subjects.objects.filter(student_id = admin_id)
    student_subject = Section_subjects.objects.filter(student_id = admin_id)
    first_qtr = First_Qtr.objects.filter(section_subject_id__in = student)
    second_qtr = Second_Qtr.objects.filter(section_subject_id__in = student)
    third_qtr = Third_Qtr.objects.filter(section_subject_id__in = student)
    fourth_qtr = Fourth_Qtr.objects.filter(section_subject_id__in = student)
    return render(request, 'student/view_grades.html', {'student_subject':student_subject, 'first_qtr':first_qtr,'second_qtr':second_qtr,'third_qtr':third_qtr,'fourth_qtr':fourth_qtr})

def view_activities(request,section_subject_id):
    current_user = request.user
    admin_id = current_user.id
    section_subject = Section_subjects.objects.filter(id= section_subject_id)
    student = Section_subjects.objects.filter(student_id = admin_id)
    homework = Homework.objects.filter(section_subject_id__in = student)
    quizzes = Quizzes.objects.filter(section_subject_id__in = student)
    seatwork = Seatwork.objects.filter(section_subject_id__in = student)
    exams = Examinations.objects.filter(section_subject_id__in = student)
    performance = Performance_Task.objects.filter(section_subject_id__in = student)
    return render(request, 'student/view_grade_details.html',{'section_subject':section_subject,'homework':homework,'quizzes':quizzes,'seatwork':seatwork,'exams':exams,'performance':performance})
