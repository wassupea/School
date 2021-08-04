from django.http.response import JsonResponse
from gms_admin.forms import *
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from gms_admin.models import *
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from .filters import *

def admin_home(request):
    teacher = Teacher.objects.filter(status=1).count()
    student = Students.objects.filter(status=1).count()
    classes = Classes.objects.filter(status=1).count()
    subjects = Subjects.objects.filter(status=1).count()
    return render(request, 'main/admin_dashboard.html', {'teacher':teacher, 'student':student, 'classes':classes, 'subjects':subjects})
    #return render (request,"main/sidebar")

def admin_chat(request):
    user = request.user.id
    all_users = CustomUser.objects.all()
    sent = Msg.objects.filter(sender_id = user).order_by('-date')
    receive = Msg.objects.filter(receiver_id = user).order_by('-date')
    return render(request, 'main/chat.html', {'all_users':all_users, 'sent':sent, 'receive':receive})

def adminsend_message(request):
    user_id = request.user.id
    sender = CustomUser.objects.get(id=user_id)
    receiver_id = request.POST.get('receiver')
    print(receiver_id)
    receiver = CustomUser.objects.get(id=receiver_id)
    body = request.POST.get('my_textarea')
    print(body)

    message_send = Msg(sender=sender, receiver=receiver, body=body)
    message_send.save()
    return redirect(request.META.get('HTTP_REFERER'))

def admin_reply(request):
    user_id = request.user.id
    sender = CustomUser.objects.get(id=user_id)
    receiver_id = request.POST.get('receiver')
    print(receiver_id)
    receiver = CustomUser.objects.get(id=receiver_id)
    body = request.POST.get('my_textarea')
    print(body)

    message_send = Msg(sender=sender, receiver=receiver, body=body)
    message_send.save()
    return HttpResponseRedirect('admin_chat')


def add_teacher(request):
    teachers = Teacher.objects.all()
    #return render(request, 'main/teacher.html', {"teachers":teachers})
    return render(request, 'main/addteacher_template.html', {"teachers":teachers})

def save_teacher(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("fname")
        last_name=request.POST.get("lname")
        #gender = request.POST.get("gender")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        SpecialSym=['$','@','#']

 

        if CustomUser.objects.filter(last_name = last_name).filter(first_name = first_name).exists() or CustomUser.objects.filter(email=email).exists():
            messages.error(request,"Failed to Add Teacher")
            return HttpResponseRedirect(reverse('add_teacher'))

        if CustomUser.objects.filter(email = email).exists() and CustomUser.objects.filter(username = username).exists():
            messages.error(request,"Failed to Add Teacher")
            return HttpResponseRedirect(reverse('add_teacher'))

        if (len(password) < 8 ):
            messages.error(request,"Password too short")
            return HttpResponseRedirect(reverse('add_teacher'))
            
        if not any(char in SpecialSym for char in password):
            messages.error(request,"Please provide special characters on your password")
            return HttpResponseRedirect(reverse('add_teacher'))

        if first_name[0].islower() or last_name[0].islower():
            messages.error(request,"Invalid Name Format")
            return HttpResponseRedirect(reverse('add_teacher'))
            
        if not last_name.isalpha():
            messages.error(request, 'Name cannot contain other characters')
            return HttpResponseRedirect(reverse("manage_teacher"))
            
        else:
            if first_name.isalpha():
                try:
                    user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
                    user.teacher.address = address
                    user.teacher.fname=first_name
                    user.teacher.lname = last_name
                    user.teacher.status = 1
                    user.save()        
                    messages.success(request,"Added Teacher")

                        #send an email
                    send_mail(
                            'Account Credentials for ' + last_name + ', ' +first_name,
                            'email: ' + email + ' password: ' + password,
                            'hwngryjn@gmail.com',
                            [email],
                            fail_silently=False,
                        )



                    return HttpResponseRedirect(reverse("manage_teacher"))
                except:
                    messages.error(request, 'Failed')
                    return HttpResponseRedirect(reverse("manage_teacher"))
            else:
                messages.error(request, 'Name cannot contain other characters')
                return HttpResponseRedirect(reverse("manage_teacher")) 
           
def add_gradelevel(request):
    gradelevels = GradeLevel.objects.all()
    return render(request, 'main/add_gradelevel.html', {"gradelevels":gradelevels})

def save_gradelevel(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        grade_level =request.POST.get("grade_level")
        if GradeLevel.objects.filter(gradeLevel_no = grade_level).exists():
            messages.error(request,"Failed to add Grade Level")
            return HttpResponseRedirect(reverse("add_gradelevel"))

        if not grade_level.isdigit():
            messages.error(request,"Invalid")
            return HttpResponseRedirect(reverse("add_gradelevel"))

        else:
            try:
                gradelevel_model = GradeLevel(gradeLevel_no=grade_level, status=1)
                print(grade_level)
                gradelevel_model.save()
                messages.success(request,"Added Grade Level")
                return HttpResponseRedirect(reverse("manage_school"))
            except:
                messages.error(request,"Invalid")
                return HttpResponseRedirect(reverse("add_gradelevel"))

def add_student(request):
    GradeLevels = GradeLevel.objects.all()
    school_year = SessionYearModel.objects.all()
    classes = Classes.objects.filter(status=1)
    #students = Students.objects.all()
    #sections = Sections.objects.all()
    form = AddStudentForm()
    return render(request, 'main/addstudent_template.html',{'GradeLevels':GradeLevels,'school_year':school_year,'classes':classes,'form':form})

def save_student2(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("fname")
        last_name=request.POST.get("lname")
        gender = request.POST.get("gender")
        gradelevel = request.POST.get("gradelevel")
        school_year = request.POST.get("school_year")
        classes = request.POST.get("classes")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        SpecialSym=['$','@','#','!']

        gradelevel_id = GradeLevel.objects.get(id=gradelevel)
        class_id = Classes.objects.get(id=classes)
        session_year_id = SessionYearModel.objects.get(id=school_year)

 

        if CustomUser.objects.filter(last_name = last_name).filter(first_name = first_name).exists()  or CustomUser.objects.filter(email=email).exists():
            messages.error(request,"Failed to Add Student")
            return HttpResponseRedirect(reverse('add_teacher'))

        if CustomUser.objects.filter(email = email).exists() and CustomUser.objects.filter(username = username).exists():
            messages.error(request,"Failed to Add Student")
            return HttpResponseRedirect(reverse('add_student'))

        if (len(password) < 8 ):
            messages.error(request,"Password too short")
            return HttpResponseRedirect(reverse('add_student'))
            
        if not any(char in SpecialSym for char in password):
            messages.error(request,"Please provide special characters on your password")
            return HttpResponseRedirect(reverse('add_student'))

        if first_name[0].islower() or last_name[0].islower():
            messages.error(request,"Invalid Name Format")
            return HttpResponseRedirect(reverse('add_student'))
            
        if not last_name.isalpha():
            messages.error(request, 'Name cannot contain other characters')
            return HttpResponseRedirect(reverse("manage_teacher"))
            
        else:
            if first_name.isalpha():
                #try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                user.students.address = address
                user.students.fname=first_name
                user.students.lname = last_name
                user.students.gradelevel_id = gradelevel_id
                user.students.gender = gender
                user.students.class_id = class_id
                user.students.session_year_id = session_year_id
                user.students.status = 1
                user.save()        
                messages.success(request,"Added Student")

                        #send an email
                send_mail(
                            'Account Credentials for ' + last_name + ', ' +first_name,
                            'email: ' + email + ' password: ' + password,
                            'hwngryjn@gmail.com',
                            [email],
                            fail_silently=False,
                        )
                print(user.id)
                add_section = Section(class_id = class_id, student_id= user)
                add_section.save()


                return HttpResponseRedirect(reverse("manage_student"))
                #except:
                    #messages.error(request, 'Failed')
                    #return HttpResponseRedirect(reverse("manage_student"))
            else:
                messages.error(request, 'Name cannot contain other characters')
                return HttpResponseRedirect(reverse("manage_student")) 

def save_student(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddStudentForm(request.POST)
        if form.is_valid():
            gradelevel_id = form.cleaned_data["grade_level"]
            class_id = form.cleaned_data["class_id"]
            first_name=form.cleaned_data["fname"]
            last_name=form.cleaned_data["lname"]
            gender = form.cleaned_data["gender"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            SpecialSym=['$','@','#', '!']
           

            if CustomUser.objects.filter(last_name = last_name).filter(first_name = first_name).exists():
                messages.error(request,"Failed to add Student")
                return HttpResponseRedirect("/add_student")

            if CustomUser.objects.filter(email = email).exists() and CustomUser.objects.filter(username = username).exists():
                messages.error(request,"Failed to add Student")
                return HttpResponseRedirect("/add_student")

            if (len(password) < 8 ):
                messages.error(request,"Password too short")
                return HttpResponseRedirect("/add_student")
                
            if not any(char in SpecialSym for char in password):
                messages.error(request,"Please provide special characters on your password")
                return HttpResponseRedirect("/add_student")

            if first_name[0].islower() or last_name[0].islower():
                messages.error(request,"Invalid Name Format")
                return HttpResponseRedirect("/add_student")

            if not last_name.isalpha():
                messages.error(request, 'Name cannot contain other characters')
                return HttpResponseRedirect("/add_student")

            if not first_name.isalpha():
                messages.error(request, 'Name cannot contain other characters')
                return HttpResponseRedirect("/add_student")
                
            else:
                try:
                    user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
                    gradelevel_obj = GradeLevel.objects.get(id=gradelevel_id)
                    class_id = Classes.objects.get(id=class_id)
                    session_year = SessionYearModel.objects.get(id=session_year_id)
                    user.students.address = address
                    user.students.gradelevel_id=gradelevel_obj
                    user.students.class_id = class_id
                    user.students.gender=gender
                    user.students.session_year_id=session_year
                    user.students.status = 1
                    user.students.fname = first_name
                    user.students.lname = last_name
                    user.save()

                    print(class_id)

                        #add to section
                    add_section = Section(class_id = class_id, student_id= user)
                    add_section.save()


                        #send an email
                    send_mail(
                        'Account Credentials for ' + last_name + ', ' +first_name,
                        'email: ' + email + ' password: ' +password,
                        'hwngryjn@gmail.com',
                        [email],
                        fail_silently=False,
                        )

                    messages.success(request,"Added Student")
                    return HttpResponseRedirect("manage_student")
                except:
                    messages.error(request,"Failed")
                    return HttpResponseRedirect("manage_student")

    

def student_home(request):
    return render(request, 'main/student_dashboard.html')

def manage_student(request):
    students = Students.objects.all()
    classes = Classes.objects.all()
    sections = Section.objects.all()
    myFilter = StudentFilter(request.GET, queryset=students)
    students = myFilter.qs
    return render(request, 'main/manage_students.html',{'students':students,'classes':classes, 'sections':sections, 'myFilter':myFilter})

def manage_teacher(request):
    teachers = Teacher.objects.all()
    myFilter = TeacherFilter(request.GET, queryset=teachers)
    teachers = myFilter.qs
    return render(request, 'main/manage_teacher.html',{'teachers':teachers, 'myFilter':myFilter})

def manage_subject(request):
    GradeLevels = GradeLevel.objects.all()
    teachers = CustomUser.objects.filter(user_type=2)
    subjects = Subjects.objects.all()
    myFilter = SubjectFilter(request.GET, queryset=subjects)
    subjects = myFilter.qs
    return render(request, 'main/manage_subject.html',{"GradeLevels":GradeLevels, "teachers":teachers,'subjects':subjects, 'myFilter':myFilter})

def add_subjects(request):
    classes = Classes.objects.filter(status=1) 
    sections = Section.objects.all()
    teacher = Teacher.objects.filter(status=1)   
    return render(request, 'main/add_subjects.html', {"classes":classes, 'teacher':teacher, 'sections':sections})

def save_subjects(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    
    else:
        subject=request.POST.get("subject")
        classes_id = request.POST.get("class_id")
        class_id=Classes.objects.get(id=classes_id)
        #sections_id = request.POST.get("section_id")
        
        #print(section_id)
        teacher = request.POST.get("teacher")
        teacher_id = CustomUser.objects.get(id=teacher)
        print(teacher)
    
        if Subjects.objects.filter(subject_name = subject).filter(class_id = class_id).exists():
            messages.error(request,"Existing Subject")
            return HttpResponseRedirect("/add_subjects")
        else:
            
            try:
                subject__in=Subjects(subject_name=subject, class_id=class_id,teacher_id=teacher_id, status=1)
                subject__in.save()
                messages.success(request,"Added Subject")
                return HttpResponseRedirect(reverse("manage_subject"))
            except:
                messages.error(request,"Failed")
                return HttpResponseRedirect("manage_subject")

        #return HttpResponse('ok')


def add_section(request, student_id):
    student = Students.objects.get(admin=student_id)
    classes = Classes.objects.all()
    return render(request, 'main/addsections.html', {'classes':classes, 'student':student})

def save_section(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    
    else:
        class_id=request.POST.get("class_id")
        class_id=Classes.objects.get(id=class_id)
        student_id=request.POST.get("student_id")
        student=CustomUser.objects.get(id=student_id)

        if Section.objects.filter(student_id = student_id).exists():
            messages.error(request,"Failed to Add Section")
            return HttpResponseRedirect("add_section")
        else:
            try:
                section=Section(class_id=class_id,student_id__in=student)
                section.save()
                messages.success(request,"Successfully Added Section")
                return HttpResponseRedirect("manage_student")

            except:
                messages.error(request,"Failed")
                return HttpResponseRedirect("manage_student")
            

def add_class(request):
    GradeLevels = GradeLevel.objects.filter(status=1)
    teachers = CustomUser.objects.filter(user_type=2)
    return render(request, 'main/addclass.html', {"GradeLevels":GradeLevels,  "teachers":teachers})

def save_class(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    
    else:
        gradelevel_id=request.POST.get("gradelevel")
        gradelevel=GradeLevel.objects.get(id=gradelevel_id)
        class_name = request.POST.get("class_name")
        teacher_id=request.POST.get("teacher")
        teacher=CustomUser.objects.get(id=teacher_id)
        
        if Classes.objects.filter(class_name = class_name).exists():
            messages.error(request,"Class exists")
            return HttpResponseRedirect(reverse("add_class"))
        else:
            try:
                class2=Classes(teacher_id=teacher,gradelevel_id=gradelevel,class_name=class_name, status=1)
                class2.save()
                messages.success(request,"Successfully Added class")
                return HttpResponseRedirect(reverse("manage_school"))
            except:
                messages.error(request,"Failed")
                return HttpResponseRedirect(reverse("add_class"))

def add_sectionsubjects(request, student_id):
    student = Students.objects.get(admin_id=student_id)
    class_id = Students.objects.filter(admin_id=student_id).values_list('class_id')
    #classes = class_id.class_id
    print(class_id)
    subjects = Subjects.objects.filter(class_id__in=class_id).filter(status=1)
    return render(request, 'main/add_class_subjects.html', {"student":student,"subjects":subjects})


def save_sectionsubjects(request):
    if request.method != 'POST':
        return HttpResponse('error')

    else:
        student_id=request.POST.get("student_id")
        print(student_id)
        student=CustomUser.objects.get(id=student_id)
        subject_id=request.POST.get("subject")
        subject_id=Subjects.objects.get(id=subject_id)


        if Section_subjects.objects.filter(subject_id=subject_id).exists() and Section_subjects.objects.filter(student_id=student).exists():
            messages.error(request,"Existing Subject")
            return redirect(request.META.get('HTTP_REFERER'))
            
            
        else:
            try:
                class_sub=Section_subjects(subject_id=subject_id, student_id=student)
                print(class_sub)
                class_sub.save()
                #return HttpResponse('OK')
                messages.success(request,"Successfully Added Subject to students")
                return HttpResponseRedirect(reverse("manage_student"))
            except:
                messages.error(request,"Failed")
                return HttpResponseRedirect(reverse("manage_student"))

    


def edit_teacher(request, teacher_id):
    teacher = Teacher.objects.get(admin_id=teacher_id)
    return render(request, "main/editteacher.html/", {"teacher":teacher})


def save_editteacher(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        teacher_id=request.POST.get("teacher_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")
        status = request.POST.get("status")


        try:
            user=CustomUser.objects.get(id=teacher_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.is_active = status
            user.save()

            teacher_model=Teacher.objects.get(admin=teacher_id)
            teacher_model.address=address
            teacher_model.status=status
            teacher_model.save()

            messages.success(request,"Successfully Edited Teacher")
            return HttpResponseRedirect(reverse("manage_teacher"))
        
        except:
        
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("manage_teacher"))


def edit_student(request, student_id):
    request.session['student_id']=student_id
    student = Students.objects.get(admin=student_id)
    gradelevel = GradeLevel.objects.all()
    classes =Classes.objects.filter(status=1)
    school_year = SessionYearModel.objects.all()
    return render(request, "main/editstudent_template.html/", {'student':student,'gradelevel':gradelevel,'classes':classes,'school_year':school_year})

def save_editstudent2(request):

    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.POST.get("student_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")
        status = request.POST.get("status")
        class_id = request.POST.get("classes")
        gradelevel_id = request.POST.get("gradelevel")
        school_year_id = request.POST.get("school_year")
        classes = Classes.objects.get(id=class_id)
        gradelevel = GradeLevel.objects.get(id=gradelevel_id)
        school_year =SessionYearModel.objects.get(id=school_year_id)
        try:
            user=CustomUser.objects.get(id=student_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            student_model=Students.objects.get(admin_id=student_id)
            student_model.address=address
            student_model.status=status
            student_model.class_id=classes
            student_model.gradelevel_id=gradelevel
            student_model.session_year_id=school_year
            student_model.save()

            section = Section.objects.get(student_id=student_id)
            section.class_id = classes
            section.save()



            messages.success(request,"Successfully Edited Student")
            return HttpResponseRedirect(reverse("manage_student"))
        
        except:
        
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_student"))


def edit_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    gradelevels = GradeLevel.objects.all()
    teachers = CustomUser.objects.filter(user_type=2)
    return render (request, 'main/edit_subjects.html/',{"subject":subject, "gradelevels": gradelevels, "teachers":teachers})


def save_editsubject(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        teacher_id=request.POST.get("teacher")
        status = request.POST.get("status")
        try:

            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            teacher=CustomUser.objects.get(id=teacher_id)
            subject.teacher_id=teacher
            subject.status = status
            subject.save()
            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("manage_subject"))

        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject"))


def edit_class(request, class_id):
    classes = Classes.objects.get(id=class_id)
    gradelevels = classes.gradelevel_id
    gradelevel = GradeLevel.objects.get(id=gradelevels)
    teachers = CustomUser.objects.filter(user_type=2)
    return render (request, 'main/edit_class.html/',{"classes":classes, "gradelevel": gradelevel, "teachers":teachers}) 

def save_editclass(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        class_id=request.POST.get("class_id")
        class_name=request.POST.get("class_name")
        teacher_id=request.POST.get("teacher")
        gradelevel_id=request.POST.get("grade_level")
        status=request.POST.get("status")
        try:

            classes=Classes.objects.get(id=class_id)
            classes.class_name=class_name
            teacher=CustomUser.objects.get(id=teacher_id)
            classes.teacher_id=teacher
            gradelevel=GradeLevel.objects.get(id=gradelevel_id)
            classes.gradelevel_id=gradelevel
            classes.status = status
            classes.save()
            messages.success(request,"Successfully Edited Class")
            return HttpResponseRedirect(reverse("manage_school"))

        except:
            messages.error(request,"Failed to Edit Class")
            return HttpResponseRedirect(reverse("edit_class"))

def edit_gradelevel(request, gradelevel_id):
    gradelevel = GradeLevel.objects.get(id=gradelevel_id)
    return render(request, "main/edit_gradelevel.html/", {"gradelevel":gradelevel})

def save_editgradelevel(request):
    gradelevel_id=request.POST.get("gradelevel_id")
    grade_level=request.POST.get("grade_level")
    status=request.POST.get("status")
    try:

            gradelevels=GradeLevel.objects.get(id=gradelevel_id)
            gradelevels.gradeLevel_no=grade_level
            gradelevels.status = status
            gradelevels.save()
            messages.success(request,"Successfully Edited Grade Level")
            return HttpResponseRedirect(reverse("manage_school"))

    except:
            messages.error(request,"Failed to Grade Level")
            return HttpResponseRedirect(reverse("manage_school"))




def delete_gradelevel(request, gradelevel_id):
    gradelevel = GradeLevel.objects.get(id=gradelevel_id)
    try:
        gradelevel.delete()
        messages.success(request,"Deleted")
    except:
        messages.error(request, 'Failed to delete')
    return HttpResponseRedirect(reverse("manage_school"))

def delete_class(request,class_id):
    gradelevel = Classes.objects.get(id=class_id)
    try:
        gradelevel.delete()
        messages.success(request,"Deleted")
    except:
        messages.error(request, 'Failed to delete')
    return HttpResponseRedirect(reverse("manage_school"))

def delete_year(request,schoolyear_id):
    gradelevel = SessionYearModel.objects.get(id=schoolyear_id)
    try:
        gradelevel.delete()
        messages.success(request,"Deleted")
    except:
        messages.error(request, 'Failed to delete')
    return HttpResponseRedirect(reverse("manage_school"))

def delete_subject(request,subject_id):
    gradelevel = Subjects.objects.get(id=subject_id)
    try:
        gradelevel.delete()
        messages.success(request,"Deleted")
    except:
        messages.error(request, 'Failed to delete')
    return HttpResponseRedirect(reverse("manage_subject"))

def delete_student(request,student_id):
    gradelevel = CustomUser.objects.get(id=student_id)
    try:
        gradelevel.delete()
        messages.success(request,"Deleted")
    except:
        messages.error(request, 'Failed to delete')
    return HttpResponseRedirect(reverse("manage_student"))

def delete_teacher(request,teacher_id):
    gradelevel = CustomUser.objects.get(id=teacher_id)
    try:
        gradelevel.delete()
        messages.success(request,"Deleted")
    except:
        messages.error(request, 'Failed to delete')
    return HttpResponseRedirect(reverse("manage_teacher"))

def manage_school(request):
    gradelevels = GradeLevel.objects.all()
    teachers = CustomUser.objects.filter(user_type=2)
    sections = Section.objects.all()
    classes = Classes.objects.all()
    school_year = SessionYearModel.objects.all()
    return render (request, 'main/manage_school.html/',{"sections":sections, "gradelevels": gradelevels, "teachers":teachers, "classes":classes,'school_year':school_year})

def add_sessionyear(request):
    return render (request, 'main/addsessionyear.html/')


def save_sessionyear(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('manage_school'))
    
    else:
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')
        
        if SessionYearModel.objects.filter(session_start_year = session_start_year).exists() and SessionYearModel.objects.filter(session_end_year = session_end_year).exists():
            messages.error(request,"Existing")
            return HttpResponseRedirect(reverse("add_sessionyear"))
        
        else:
            try:
                session = SessionYearModel(session_start_year =session_start_year,session_end_year=session_end_year )
                session.save()
                messages.success(request,"Added")
                return HttpResponseRedirect(reverse("manage_school"))
            except:
                messages.error(request,"Failed")
                return HttpResponseRedirect(reverse("manage_school"))



def sections(request):
    sections = Section.objects.all()
    classes = Classes.objects.filter(status=1)
    session_year = SessionYearModel.objects.all()
    return render (request, 'main/section.html', {'sections':sections, 'classes':classes,'session_year':session_year})

@csrf_exempt
def get_section(request):
    class_id = request.POST.get("classes")
    section = Section.objects.filter(class_id__in=class_id)
    #section_data = serializers.serialize("python", section)
    list_data=[]

    for sections in section:
        data_small ={"gradelevel":sections.class_id.gradelevel_id_id, "class_name":sections.class_id.class_name,"name":sections.student_id.first_name +" " +sections.student_id.last_name, "teacher_name":sections.class_id.teacher_id.first_name +" "+ sections.class_id.teacher_id.last_name }
        list_data.append(data_small)
        print(list_data)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def add_admin(request):
    return render (request, 'main/addparents.html')

def save_admin(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("fname")
        last_name=request.POST.get("lname")
        #gender = request.POST.get("gender")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        SpecialSym=['$','@','#']

 

        if CustomUser.objects.filter(last_name = last_name).filter(first_name = first_name).exists():
            messages.error(request,"Failed to Add Teacher")
            return HttpResponseRedirect(reverse('add_teacher'))

        if CustomUser.objects.filter(email = email).exists() and CustomUser.objects.filter(username = username).exists():
            messages.error(request,"Failed to Add Teacher")
            return HttpResponseRedirect(reverse('add_teacher'))

        if (len(password) < 8 ):
            messages.error(request,"Password too short")
            return HttpResponseRedirect(reverse('add_teacher'))
            
        if not any(char in SpecialSym for char in password):
            messages.error(request,"Please provide special characters on your password")
            return HttpResponseRedirect(reverse('add_teacher'))

        if first_name[0].islower() or last_name[0].islower():
            messages.error(request,"Invalid Name Format")
            return HttpResponseRedirect(reverse('add_teacher'))
            
        if not last_name.isalpha():
            messages.error(request, 'Name cannot contain other characters')
            return HttpResponseRedirect(reverse("manage_teacher"))
            
        else:
            if first_name.isalpha():
                try:
                    user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=1)
                    user.save()        
                    messages.success(request,"Added Teacher")

                        #send an email
                    send_mail(
                            'Account Credentials for ' + last_name + ', ' +first_name,
                            'email: ' + email + ' password: ' + password,
                            'hwngryjn@gmail.com',
                            [email],
                            fail_silently=False,
                        )



                    return HttpResponseRedirect(reverse("manage_teacher"))
                except:
                    messages.error(request, 'Failed')
                    return HttpResponseRedirect(reverse("manage_teacher"))
            else:
                messages.error(request, 'Name cannot contain other characters')
                return HttpResponseRedirect(reverse("manage_teacher")) 

def reply(request,reply_id):
    user = request.user.id
    all_users = CustomUser.objects.all()
    msg = Msg.objects.get(id=reply_id)
    return render(request, 'main/reply.html', {'all_users':all_users,'msg':msg})
