from django.forms.models import ModelForm
from django.http import request
from django.urls.base import reverse
from django.views.decorators import csrf
from gms_admin.forms import AddAnnouncement
from gms_admin.studentViews import student_subjects
from django.db.models.aggregates import Avg, Count
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from gms_admin.models import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json
from django.core import serializers
from django.contrib import messages
from django.shortcuts import redirect

def teacher_home(request):
    return render(request, 'main/teacher_dashboard.html')

def view_class(request):
    current_user = request.user
    admin_id = current_user.id
    class_id = Classes.objects.all().filter(teacher_id = admin_id)
    classes = Classes.objects.all().filter(teacher_id=admin_id)
    section = Section.objects.filter(class_id__in=class_id)
    session_year = SessionYearModel.objects.all()
    return render(request, 'teacher/html.html', {'section':section, 'classes':classes, 'session_year':session_year})

def view_subjects(request):
    current_user = request.user
    teacher_id = current_user.id
    subjects = Subjects.objects.filter(teacher_id=teacher_id)
    return render(request, 'teacher/subjects.html', {'subjects':subjects})


def attendance(request):
    current_user = request.user
    admin_id = current_user.id
    class_id = Classes.objects.all().filter(teacher_id = admin_id)
    classes = Classes.objects.all().filter(teacher_id=admin_id)
    section = Section.objects.filter(class_id__in=class_id)
    session_year = SessionYearModel.objects.all()
    return render(request, 'teacher/attendance.html', {'section':section, 'classes':classes, 'session_year':session_year})


@csrf_exempt
def get_students(request):
    class_id = request.POST.get("classes")
    section = Section.objects.filter(class_id__in=class_id)
    list_data=[]

    for sections in section:
        data_small ={"gradelevel":sections.class_id_id, "id":sections.student_id_id,"name":sections.student_id.first_name +" " +sections.student_id.last_name }
        list_data.append(data_small)
        print(list_data)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def save_attendance(request):
    student_ids=request.POST.get("student_ids")
    class_id=request.POST.get("class_id")
    attendance_date=request.POST.get('attendance_date')
    dict_student =json.loads(student_ids)
    session_year_id=request.POST.get("session_year_id")
    print(session_year_id)

    class_model = Classes.objects.get(id=class_id)
    session_model = SessionYearModel.objects.get(id=session_year_id)
    attendance = Attendance(class_id=class_model, session_year_id=session_model,attendance_date=attendance_date)
    attendance.save()

    for student in dict_student:
        students = Students.objects.get(admin=student['id'])
        attendance_report = AttendanceReport(student_id=students, attendance_id=attendance,status=student['status'])
        attendance_report.save()
    return HttpResponse('OK')

def update_attendance(request):
    current_user = request.user
    admin_id = current_user.id
    class_id = Classes.objects.all().filter(teacher_id = admin_id)
    classes = Classes.objects.all().filter(teacher_id=admin_id)
    section = Section.objects.filter(class_id__in=class_id)
    session_year = SessionYearModel.objects.all()
    return render(request, 'teacher/update_attendance.html', {'classes':classes,'section':section,'session_year':session_year} )

@csrf_exempt
def get_attendance(request):
    classes = request.POST.get('classes')
    session_year_id = request.POST.get('session_year_id')
    class_id=Classes.objects.get(id=classes)
    session_obj=SessionYearModel.objects.get(id=session_year_id)
    attendance = Attendance.objects.filter(class_id=class_id, session_year_id=session_obj)
    attendance_obj=[]

    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def get_attendance_students(request):
    attendance_date=request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for sections in attendance_data:
        data_small ={"gradelevel":sections.student_id.gradelevel_id_id, "id":sections.student_id.admin.id,"name":sections.student_id.admin.first_name +" " +sections.student_id.admin.last_name, 'status':sections.status}
        list_data.append(data_small)
        print(list_data)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_update_attendance(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get('attendance_date')
    dict_student =json.loads(student_ids)
    attendance = Attendance.objects.get(id=attendance_date)
   
    for student in dict_student:
        students = Students.objects.get(admin=student['id'])
        attendance_report = AttendanceReport.objects.filter(student_id=students, attendance_id=attendance)
        for object in attendance_report:
            object.status = student['status']
            object.save()
    return HttpResponse('OK')

def grade(request):
    current_user = request.user
    admin_id = current_user.id
    class_id = Classes.objects.all().filter(teacher_id = admin_id)
    subjects = Subjects.objects.all().filter(teacher_id=admin_id)
    subject_id= request.POST.get('subject')
    section_subjects = Section_subjects.objects.all().filter(id=subject_id)
    print(section_subjects)
    return render(request, 'teacher/add_grade.html', {'subjects':subjects, 'class_id':class_id, 'section_subjects':section_subjects})

@csrf_exempt
def get_subject_students(request):
    subject_id= request.POST.get('subject')
    print(subject_id)
    subjects = Section_subjects.objects.all().filter(subject_id__in=subject_id)
    list_data=[]
    
    for subject in subjects:
        data_small ={"grade_level":subject.subject_id.class_id_id, "id":subject.id,"name":subject.student_id.first_name +" " +subject.student_id.last_name, "subject_name":subject.subject_id.subject_name, "section":subject.subject_id.class_id.class_name }
        list_data.append(data_small)
        print(list_data)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

def add_activity(request, section_subject_id):
    qtr_tab = request.POST.get('qtr_tab')
    student_subject = Section_subjects.objects.get(id=section_subject_id)
    homework = Homework.objects.all().filter(section_subject_id = student_subject)
    quiz = Quizzes.objects.all().filter(section_subject_id = student_subject)
    sw = Seatwork.objects.all().filter(section_subject_id = student_subject)
    performance = Performance_Task.objects.all().filter(section_subject_id = student_subject)
    exam = Examinations.objects.all().filter(section_subject_id = student_subject)
    return render(request, 'teacher/grade_table.html', {'student_subject':student_subject,'homework':homework,'quiz':quiz,'sw':sw,'performance':performance,'exam':exam})

@csrf_exempt
def get_sectionsubject(request):
    current_user = request.user
    admin_id = current_user.id
    subject_id= request.POST.get('subject')
    subjects = Section_subjects.objects.all().filter(id=subject_id)
    print(subjects)
    list_data=[]
    
    for subject in subjects:
        data_small ={"grade_level":subject.subject_id.class_id_id, "id":subject.id,"name":subject.student_id.first_name +" " +subject.student_id.last_name, "subject_name":subject.subject_id.subject_name, "section":subject.subject_id.class_id.class_name }
        list_data.append(data_small)
        print(list_data)
    return HttpResponse('<h1>list_data</h1>')

def announcement(request):
    subjects = Subjects.objects.all()
    form = AddAnnouncement()
    return render(request, 'teacher/announcement.html', {subjects:subjects,'form':form})

def save_announcement(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddAnnouncement(request.POST)
        if form.is_valid():
            subject_id = form.cleaned_data["subject_id"]
            title=form.cleaned_data["title"]
            content=form.cleaned_data["content"]
            subject_id = Subjects.objects.get(id=subject_id)
            
            announce = Announcements(subject_id=subject_id, title=title,content=content)
            announce.save()
            return HttpResponse ('OK')

def chat(request):
    return render(request, 'teacher/chat.html')

def add_homework(request):
    if request.method == 'POST':
        qtr= request.POST.get("qtr")
        student_subject = request.POST.get("student_subject_id")
        student_subject = Section_subjects.objects.get(id=student_subject)
        hw1 = request.POST.get("hw1")
        hw1_grade = request.POST.get("hw1_grade")
        hw1_grade_max = request.POST.get("hw1_grade_max")
        hw_qtr = int(qtr)
        hw_date = request.POST.get('hw1_date')
   
        hw1_grade = int(hw1_grade)
        hw1_grade_max = int(hw1_grade_max)
        
        if Homework.objects.filter(name=hw1).filter(qtr=hw_qtr).filter(section_subject_id=student_subject).exists():
            messages.error(request,"Existing Homework")
            return redirect(request.META.get('HTTP_REFERER'))
                
        else:
            if hw1_grade_max >= hw1_grade:
                hw1_score = (hw1_grade / hw1_grade_max) * 100
                homeworks=Homework(name=hw1,section_subject_id = student_subject,raw_score=hw1_grade, items=hw1_grade_max, score=hw1_score,qtr=hw_qtr,date=hw_date)
              
                homeworks.save()
                messages.success(request,"Added Homework")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request,"Invalid")
                return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
def add_quiz(request):
    if request.method == 'POST':
        qtr= request.POST.get("qtr")
        student_subject = request.POST.get("student_subject_id")
        student_subject = Section_subjects.objects.get(id=student_subject)
        qz1 = request.POST.get("qz1")
        qz1_grade = request.POST.get("qz1_grade")
        qz1_grade_max = request.POST.get("qz1_grade_max")
        qz_qtr = int(qtr)
        date = request.POST.get('qz1_date')

        qz1_grade = int(qz1_grade)
        qz1_grade_max = int(qz1_grade_max)
        
        if Quizzes.objects.filter(name=qz1).filter(section_subject_id = student_subject).filter(qtr = qz_qtr).exists():
            messages.error(request,"Existing Quiz")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            if qz1_grade_max >= qz1_grade:
                qz1_score = (qz1_grade / qz1_grade_max) * 100
                quizzes=Quizzes(name=qz1,section_subject_id = student_subject, raw_score =qz1_grade, items=qz1_grade_max, score=qz1_score,qtr=qz_qtr,date=date)
             
                quizzes.save()
                messages.success(request,"Added Quiz")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request,"Invalid")
                return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))

def add_seatwork(request):
    if request.method == 'POST':
        qtr= request.POST.get("qtr")
        student_subject = request.POST.get("student_subject_id")
        student_subject = Section_subjects.objects.get(id=student_subject)
        sw1 = request.POST.get("sw1")
        sw1_grade = request.POST.get("sw1_grade")
        sw1_grade_max = request.POST.get("sw1_grade_max")
        sw_qtr = int(qtr)
        date = request.POST.get('sw1_date')

        sw1_grade = int(sw1_grade)
        sw1_grade_max = int(sw1_grade_max)
        
        if Seatwork.objects.filter(name=sw1).filter(section_subject_id = student_subject).filter(qtr=sw_qtr).exists():
            messages.error(request,"Existing Seatwork")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            if sw1_grade_max >= sw1_grade:
                sw1_score = (sw1_grade / sw1_grade_max) * 100
                seatworks=Seatwork(name=sw1,section_subject_id = student_subject,raw_score=sw1_grade, items=sw1_grade_max,score=sw1_score,qtr=sw_qtr,date=date)
                
                seatworks.save()
                messages.success(request,"Added Seatwork")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request,"Invalid")
                return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))

def add_exam(request):
    if request.method == 'POST':
        qtr= request.POST.get("qtr")
        student_subject = request.POST.get("student_subject_id")
        student_subject = Section_subjects.objects.get(id=student_subject)
        exam = request.POST.get("exam1")
        exam_grade = request.POST.get("exam1_grade")
        exam_grade_max = request.POST.get("exam1_grade_max")
        exam_qtr = int(qtr)
        date = request.POST.get('exam1_date')

        exam_grade = int(exam_grade)
        exam_grade_max = int(exam_grade_max)
        
        if Examinations.objects.filter(name=exam).filter(section_subject_id = student_subject).filter(qtr=exam_qtr).exists():
            messages.error(request,"Existing Exam")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            if exam_grade_max >= exam_grade:
                exam_score = (exam_grade / exam_grade_max) * 100
                exams=Examinations(name=exam,section_subject_id = student_subject, raw_score=exam_grade, items=exam_grade_max, score=exam_score,qtr=exam_qtr,date=date)
               
                exams.save()
                messages.success(request,"Added Exam")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request,"Invalid")
                return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))

def add_performance(request):
    if request.method == 'POST':
        qtr= request.POST.get("qtr")
        student_subject = request.POST.get("student_subject_id")
        student_subject = Section_subjects.objects.get(id=student_subject)
        pf = request.POST.get("pf1")
        pf_grade = request.POST.get("pf1_grade")
        pf_grade_max = request.POST.get("pf1_grade_max")
        pf_qtr = int(qtr)
        date = request.POST.get('pf1_date')
        pf_grade = int(pf_grade)
        pf_grade_max = int(pf_grade_max)
        
        if Performance_Task.objects.filter(name=pf).filter(section_subject_id = student_subject).filter(qtr=pf_qtr).exists():
            messages.error(request,"Existing Seatwork")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            if pf_grade_max >= pf_grade:
                pf_score = (pf_grade / pf_grade_max) * 100
                pfs=Performance_Task(name=pf,section_subject_id = student_subject,raw_score=pf_grade,items=pf_grade_max, score=pf_score,qtr=pf_qtr,date=date)
                
                pfs.save()
                messages.success(request,"Added Performance Task")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request,"Invalid")
                return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


    
    

@csrf_exempt
def get_homework(request):
    qtr = request.POST.get('selectedVal')
    student = request.POST.get('student')
    homework = Homework.objects.all().filter(section_subject_id = student).filter(qtr=qtr)
    list_data=[]
    
    for homework in homework:
        data_small ={"name":homework.name, "score":homework.score}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

    

@csrf_exempt
def get_quiz(request):
    qtr = request.POST.get('selectedVal')
    student = request.POST.get('student')
    quiz = Quizzes.objects.all().filter(section_subject_id = student).filter(qtr=qtr)
    list_data=[]
    
    for quiz in quiz:
        data_small ={"name":quiz.name, "score":quiz.score}
        list_data.append(data_small)
        
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)



@csrf_exempt
def get_seatwork(request):
    qtr = request.POST.get('selectedVal')
    student = request.POST.get('student')
    seatwork = Seatwork.objects.all().filter(section_subject_id = student).filter(qtr=qtr)
    list_data=[]
    
    for seatwork in seatwork:
        data_small ={"name":seatwork.name, "score":seatwork.score}
        list_data.append(data_small)
        
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def get_performance(request):
    qtr = request.POST.get('selectedVal')
    print(qtr)
    student = request.POST.get('student')
    print(student)
    performance = Performance_Task.objects.all().filter(section_subject_id = student).filter(qtr=qtr)
    list_data=[]
    
    for performance in performance:
        data_small ={"name":performance.name, "score":performance.score}
        list_data.append(data_small)
       
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def get_exam(request):
    qtr = request.POST.get('selectedVal')
    print(qtr)
    student = request.POST.get('student')
    print(student)
    exams = Examinations.objects.all().filter(section_subject_id = student).filter(qtr=qtr)
    list_data=[]
    
    for performance in exams:
        data_small ={"name":performance.name, "score":performance.score}
        list_data.append(data_small)
       
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)



def save_grade(request):
    if request.method == 'POST':
        qtr = request.POST.get('qtr')
        student = request.POST.get('student_subject_id')
        student_subject = Section_subjects.objects.get(id=student)
        grade = request.POST.get('final_grade')
        float_grade = float(grade)
        int_grade = int(float_grade)
        print(int_grade)
        qtr = int(qtr)

        if qtr == 1:
            if First_Qtr.objects.filter(qtr=qtr).exists():
                messages.error('Existing')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                first_qtr = First_Qtr(section_subject_id = student_subject, grade=int_grade )
                first_qtr.save()
                return redirect(request.META.get('HTTP_REFERER'))

        elif qtr == 2:
            if First_Qtr.objects.filter(qtr=qtr).exists():
                messages.error('Existing')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                second_qtr = Second_Qtr(section_subject_id = student_subject, grade=int_grade )
                second_qtr.save()
                return redirect(request.META.get('HTTP_REFERER'))

        elif qtr == 3:
            if First_Qtr.objects.filter(qtr=qtr).exists():
                messages.error('Existing')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                third_qtr = Third_Qtr(section_subject_id = student_subject, grade=int_grade )
                third_qtr.save()
                return redirect(request.META.get('HTTP_REFERER'))

        elif qtr == 4:
            if First_Qtr.objects.filter(qtr=qtr).exists():
                messages.error('Existing')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                fourth_qtr = Fourth_Qtr(section_subject_id = student_subject, grade=int_grade )
                fourth_qtr.save()
                return redirect(request.META.get('HTTP_REFERER'))

        else:
            return redirect(reverse('teacher_home'))

def edit_homework(request, homework_id):
    hw = Homework.objects.get(id=homework_id)
    return render(request, 'teacher/edit_homework.html/',{"hw":hw})

def edit_quiz(request,quiz_id):
    quiz = Quizzes.objects.get(id=quiz_id)
    return render(request, 'teacher/edit_quiz.html/',{"quiz":quiz})

def edit_seatwork(request,seatwork_id):
    sw = Seatwork.objects.get(id=seatwork_id)
    return render(request, 'teacher/edit_seatwork.html/',{"sw":sw})

def edit_exam(request,exam_id):
    exam = Examinations.objects.get(id=exam_id)
    return render(request, 'teacher/edit_exam.html/',{"exam":exam})

def edit_performance(request,performance_id):
    performance = Performance_Task.objects.get(id=performance_id)
    return render(request, 'teacher/edit_performance.html/',{"performance":performance})

def save_edithomework(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        hw_id=request.POST.get("homework_id")
        hw_qtr = request.POST.get('qtr')
        hw_name=request.POST.get("hw1")
        hw_raw=request.POST.get("hw1_grade")
        hw_item = request.POST.get('hw1_grade_max')
        hw_date = request.POST.get('hw1_date')
        student = request.POST.get('student_subject')
        hws=Homework.objects.get(id=hw_id)
        
        raw = int(hw_raw)
        item =int(hw_item)
        qtr = int(hw_qtr)

        if item>=raw:
            score = (raw/item) * 100
            print(hws)
            student = Section_subjects.objects.get(id=student)
            print(student)
            hws.name =hw_name
            hws.raw_score = raw
            hws.section_subject_id = student
            hws.items = item
            hws.score = score
            hws.qtr = qtr
            hws.date = hw_date
              
            hws.save()
            messages.success(request,"Added Homework")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request,"Invalid")
            return redirect(request.META.get('HTTP_REFERER'))


def save_editquiz(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        qz_id=request.POST.get("quiz_id")
        qz_qtr = request.POST.get('qtr')
        qz_name=request.POST.get("qz1")
        qz_raw=request.POST.get("qz1_grade")
        qz_item = request.POST.get('qz1_grade_max')
        qz_date = request.POST.get('qz1_date')
        student = request.POST.get('student_subject_id')
        qzs=Quizzes.objects.get(id=qz_id)
        
        raw = int(qz_raw)
        item =int(qz_item)
        qtr = int(qz_qtr)

        if item>=raw:
            score = (raw/item) * 100
            print(qzs)
            student = Section_subjects.objects.get(id=student)
            print(student)
            qzs.name =qz_name
            qzs.raw_score = raw
            qzs.section_subject_id = student
            qzs.items = item
            qzs.score = score
            qzs.qtr = qtr
            qzs.date = qz_date
              
            qzs.save()
            messages.success(request,"Updated Quiz")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request,"Invalid")
            return redirect(request.META.get('HTTP_REFERER'))

def save_editseatwork(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        sw_id=request.POST.get("sw_id")
        sw_qtr = request.POST.get('qtr')
        sw_name=request.POST.get("sw1")
        sw_raw=request.POST.get("sw1_grade")
        sw_item = request.POST.get('sw1_grade_max')
        sw_date = request.POST.get('sw1_date')
        student = request.POST.get('student_subject_id')
        sws=Seatwork.objects.get(id=sw_id)
        
        raw = int(sw_raw)
        item =int(sw_item)
        qtr = int(sw_qtr)

        if item>=raw:
            score = (raw/item) * 100
            print(sws)
            student = Section_subjects.objects.get(id=student)
            print(student)
            sws.name =sw_name
            sws.raw_score = raw
            sws.section_subject_id = student
            sws.items = item
            sws.score = score
            sws.qtr = qtr
            sws.date = sw_date
              
            sws.save()
            messages.success(request,"Updated Seatwork")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request,"Invalid")
            return redirect(request.META.get('HTTP_REFERER'))

def save_editexam(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        exam_id=request.POST.get("exam_id")
        exam_qtr = request.POST.get('qtr')
        exam_name=request.POST.get("exam1")
        exam_raw=request.POST.get("exam1_grade")
        exam_item = request.POST.get('exam1_grade_max')
        exam_date = request.POST.get('exam1_date')
        student = request.POST.get('student_subject_id')
        sws=Examinations.objects.get(id=exam_id)
        
        raw = int(exam_raw)
        item =int(exam_item)
        qtr = int(exam_qtr)

        if item>=raw:
            score = (raw/item) * 100
            print(sws)
            student = Section_subjects.objects.get(id=student)
            print(student)
            sws.name =exam_name
            sws.raw_score = raw
            sws.section_subject_id = student
            sws.items = item
            sws.score = score
            sws.qtr = qtr
            sws.date = exam_date
              
            sws.save()
            messages.success(request,"Updated Examination")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request,"Invalid")
            return redirect(request.META.get('HTTP_REFERER'))

def save_editperformance(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        exam_id=request.POST.get("pf_id")
        exam_qtr = request.POST.get('qtr')
        exam_name=request.POST.get("pf1")
        exam_raw=request.POST.get("pf1_grade")
        exam_item = request.POST.get('pf1_grade_max')
        exam_date = request.POST.get('pf1_date')
        student = request.POST.get('student_subject_id')
        sws=Performance_Task.objects.get(id=exam_id)
        
        raw = int(exam_raw)
        item =int(exam_item)
        qtr = int(exam_qtr)

        if item>=raw:
            score = (raw/item) * 100
            print(sws)
            student = Section_subjects.objects.get(id=student)
            print(student)
            sws.name =exam_name
            sws.raw_score = raw
            sws.section_subject_id = student
            sws.items = item
            sws.score = score
            sws.qtr = qtr
            sws.date = exam_date
              
            sws.save()
            messages.success(request,"Updated Performance Task")
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request,"Invalid")
            return redirect(request.META.get('HTTP_REFERER'))


