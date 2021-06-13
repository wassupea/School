from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from gms_admin.models import *
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers

def teacher_home(request):
    return render(request, 'main/teacher_dashboard.html')
    #return render (request,"main/sidebar")


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
    #section_data = serializers.serialize("python", section)
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
    #print(dict_student[0]['id'])
    session_year_id=request.POST.get("session_year_id")
    print(session_year_id)
    
    #print(student_ids)

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
    #attendance = Attendance.objects.all()
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
    #return HttpResponse('hi')
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_update_attendance(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get('attendance_date')
    #print(attendance_date)
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
    return render(request, 'teacher/add_grade.html', {'subjects':subjects, 'class_id':class_id})

@csrf_exempt
def get_subject_students(request):
    current_user = request.user
    admin_id = current_user.id
    subject_id= request.POST.get('subject')
    subjects = Section_subjects.objects.all().filter(id__in=subject_id)
    print(subjects)
    #class_id = request.POST.get("classes")
    #section = Section.objects.filter(class_id__in=class_id)
    #print(section)
    #subject_data = serializers.serialize("python", subjects)
    list_data=[]
    
    for subject in subjects:
        data_small ={"grade_level":subject.subject_id.class_id_id, "id":subject.student_id_id,"name":subject.student_id.first_name +" " +subject.student_id.last_name, "subject_name":subject.subject_id.subject_name, "section":subject.subject_id.class_id.class_name }
        list_data.append(data_small)
        print(list_data)
    #return HttpResponse('OK')
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)
    

    

