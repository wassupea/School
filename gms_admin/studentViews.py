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
    class_id = student.class_id
    subjects = Subjects.objects.filter(class_id=class_id)
    return render(request, 'student/subjects.html', {'subjects':subjects})


def view_attendance(request):
    return render(request)