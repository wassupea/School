from django.db import models
from django.db.models.base import Model
from django.db.models.fields import IntegerField
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField

# Create your models here.


class CustomUser(AbstractUser):
    user_type_data = ((1, "GMS_ADMIN"), (2, "Teacher"), (3, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class GMS_Admin(models.Model):
    id = models.AutoField(primary_key =True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    objects = models.Manager()

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year =models.DateField()
    session_end_year = models.DateField()

class GradeLevel(models.Model):
    id = models.AutoField(primary_key=True)
    gradeLevel_no = models.IntegerField(default=1)
    gradelevel_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
class Teacher(models.Model):
    id = models.AutoField(primary_key =True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Classes(models.Model):
    id = models.AutoField(primary_key=True)
    gradelevel_id = models.ForeignKey(GradeLevel, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Section(models.Model):
    id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #subject_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    objects = models.Manager()

class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=50)
    gradelevel_id = models.ForeignKey(GradeLevel, on_delete=models.CASCADE, default=1)
    #section_id = models.ForeignKey(Section,blank=True, on_delete=models.CASCADE)
    class_id =  models.ForeignKey(Classes, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Subject_Percentage(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id= models.ForeignKey(GradeLevel, on_delete=models.CASCADE)
    sw_percentage = models.IntegerField()
    hw_percentage = models.IntegerField()
    qz_percentage = models.IntegerField()
    objects = models.Manager()

class Section_subjects(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    objects = models.Manager()


class Parents(models.Model):
    id = models.AutoField(primary_key =True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Students(models.Model):
    id = models.AutoField(primary_key =True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    gradelevel_id = models.ForeignKey(GradeLevel, on_delete=models.DO_NOTHING)
    class_id = models.ForeignKey(Classes, on_delete=models.DO_NOTHING)
    gender = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    




class Attendance(models.Model):
    id = models.AutoField(primary_key =True)
    class_id = models.ForeignKey(Classes, on_delete=models.CASCADE)
    #section_id = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    attendance_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    id = models.AutoField(primary_key =True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default =False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Quizzes(models.Model):
    id = models.AutoField(primary_key =True)
    section_subject_id = models.ForeignKey(Section_subjects, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    raw_score = models.IntegerField()
    score = models.IntegerField()
    items = models.IntegerField()
    qtr = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    objects = models.Manager()

class Homework(models.Model):
    id = models.AutoField(primary_key =True)
    section_subject_id = models.ForeignKey(Section_subjects, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    raw_score = models.IntegerField()
    items = models.IntegerField()
    score = models.IntegerField()
    qtr = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    objects = models.Manager()

class Seatwork(models.Model):
    id = models.AutoField(primary_key =True)
    section_subject_id = models.ForeignKey(Section_subjects, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    raw_score = models.IntegerField()
    items = models.IntegerField()
    score = models.IntegerField()
    qtr = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    objects = models.Manager()

class Examinations(models.Model):
    id = models.AutoField(primary_key =True)
    section_subject_id = models.ForeignKey(Section_subjects, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    raw_score = models.IntegerField()
    items = models.IntegerField()
    score = models.IntegerField()
    qtr = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    objects = models.Manager()

class Performance_Task (models.Model):
    id = models.AutoField(primary_key =True)
    section_subject_id = models.ForeignKey(Section_subjects, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    raw_score = models.IntegerField()
    items = models.IntegerField()
    score = models.IntegerField()
    qtr = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    objects = models.Manager()


class First_Qtr(models.Model):
    id = models.AutoField(primary_key =True)
    section_subject_id = models.ForeignKey(Section_subjects, on_delete=models.DO_NOTHING)
    grade= models.IntegerField()
    objects = models.Manager()

class Second_Qtr(models.Model):
    id = models.AutoField(primary_key =True)
    section_subject_id = models.ForeignKey(Section_subjects, on_delete=models.DO_NOTHING)
    grade= models.IntegerField()
    objects = models.Manager()

class Third_Qtr(models.Model):
    id = models.AutoField(primary_key =True)
    section_subject_id = models.ForeignKey(Section_subjects, on_delete=models.DO_NOTHING)
    grade= models.IntegerField()
    objects = models.Manager()

class Fourth_Qtr(models.Model):
    id = models.AutoField(primary_key =True)
    section_subject_id = models.ForeignKey(Section_subjects, on_delete=models.DO_NOTHING)
    grade= models.IntegerField()
    objects = models.Manager()






class Announcements(models.Model):
    id = models.AutoField(primary_key =True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    title = models.TextField()
    content = RichTextField(blank=True,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    ordering = ['date_added']



#adding new row in admin, teacher, student with its ID
@receiver(post_save, sender=CustomUser)
def create_user(sender,instance, created, **kwargs):
    #assigning user types
    if created:
        if instance.user_type == 1:
            GMS_Admin.objects.create(admin=instance)

        if instance.user_type == 2:
            Teacher.objects.create(admin=instance)

        if instance.user_type == 3:
            Students.objects.create(admin=instance, gradelevel_id = GradeLevel.objects.get(id=1), session_year_id=SessionYearModel.objects.get(id=1), class_id = Classes.objects.get(id=1),  address="",gender="")

@receiver(post_save, sender=CustomUser)
def save_user(sender, instance, created, **kwargs):
    if instance.user_type == 1:
        instance.gms_admin.save()
    if instance.user_type == 2:
        instance.teacher.save()
    if instance.user_type == 3:
        instance.students.save()
    


    


