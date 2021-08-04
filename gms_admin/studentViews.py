from django.contrib import admin, messages
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from gms_admin.models import*
from django.shortcuts import redirect, render


def student_home(request):
    current_user = request.user
    admin_id = current_user.id
    student = Students.objects.get(admin_id=admin_id)
    student_section = CustomUser.objects.get(id=admin_id)
    section = Section.objects.get(student_id = student_section)
    print(section)
    student_subjects = Section_subjects.objects.filter(student_id = admin_id).count()
    return render(request, 'main/student_dashboard.html', {'student_subjects':student_subjects, 'student':student, 'section':section})


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
    post = Announcements.objects.filter(subject_id__in=subjects).order_by('-date_added')
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
    final_qtr = Final_Grade.objects.filter(section_subject_id__in = student)
    print(first_qtr, second_qtr,third_qtr,fourth_qtr)
    return render(request, 'student/view_grades.html', {'student_subject':student_subject, 'first_qtr':first_qtr,'second_qtr':second_qtr,'third_qtr':third_qtr,'fourth_qtr':fourth_qtr,'final_qtr':final_qtr})


def view_grades_details(request):
    current_user = request.user
    admin_id = current_user.id
    
    student = Section_subjects.objects.filter(student_id = admin_id)
    student_subject = Section_subjects.objects.filter(student_id = admin_id)
    first_qtr = First_Qtr.objects.filter(section_subject_id__in = student)
    second_qtr = Second_Qtr.objects.filter(section_subject_id__in = student)
    third_qtr = Third_Qtr.objects.filter(section_subject_id__in = student)
    fourth_qtr = Fourth_Qtr.objects.filter(section_subject_id__in = student)
    final_qtr = Final_Grade.objects.filter(section_subject_id__in = student)
    return render(request, 'student/view_grades.html', {'student_subject':student_subject, 'first_qtr':first_qtr,'second_qtr':second_qtr,'third_qtr':third_qtr,'fourth_qtr':fourth_qtr, 'final_qtr':final_qtr})

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

def chat(request):
    user = request.user.id
    all_users = CustomUser.objects.all()
    sent = Msg.objects.filter(sender_id = user).order_by('-date')
    receive = Msg.objects.filter(receiver_id = user).order_by('-date')
    return render(request, 'student/chat.html', {'all_users':all_users, 'sent':sent, 'receive':receive})

def send_message(request):
    user_id = request.user.id
    sender = CustomUser.objects.get(id=user_id)
    receiver_id = request.POST.get('receiver')
    receiver = CustomUser.objects.get(id=receiver_id)
    body = request.POST.get('my_textarea')
    print(body)
    try:
        message_send = Msg(sender=sender, receiver=receiver, body=body)
        message_send.save()
        return HttpResponseRedirect(reverse('student_chat'))
    except:
        messages.error(request, 'error')
        return HttpResponseRedirect('chat')

def student_reply(request,reply_id):
    user = request.user.id
    all_users = CustomUser.objects.all()
    msg = Msg.objects.get(id=reply_id)
    return render(request, 'student/reply.html', {'all_users':all_users,'msg':msg})
