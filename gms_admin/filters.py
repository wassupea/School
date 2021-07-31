from django.db.models import fields
import django_filters
from django_filters import filters

from .models import *

class TeacherFilter(django_filters.FilterSet):
    Status_Choices =  (
    ('1','Active'),
    ('0','Inactive'),
    ('','Any'),
)
    fname = django_filters.CharFilter(field_name="fname",lookup_expr='iexact', label='First Name')
    lname = django_filters.CharFilter(field_name="lname",lookup_expr='iexact', label='Last Name')
    status = django_filters.ChoiceFilter(choices=Status_Choices,label='Status')

    class Meta:
        model = Students
        fields = ['fname','lname','status']
        exclude = ['admin','class_id', 'session_year_id','address', 'created_at', 'updated_at']

class SubjectFilter(django_filters.FilterSet):
    Status_Choices =  (
    ('1','Active'),
    ('0','Inactive'),
    ('','Any'),
)
    classes = Classes.objects.all()
    teacher = Teacher.objects.all()
    teacher_id = filters.ModelChoiceFilter(queryset=teacher,label='Teacher')
    subject_name = django_filters.CharFilter(field_name="subject_name",lookup_expr='iexact', label='Subject Name')
    class_id = filters.ModelChoiceFilter(queryset=classes,label='Class')
    status = django_filters.ChoiceFilter(choices=Status_Choices,label='Status')
    class Meta:
        model = Subjects
        fields = ['subject_name','class_id','teacher_id','status']
        exclude = ['gradelevel_id', 'created_at', 'updated_at']

class StudentFilter(django_filters.FilterSet):
    Status_Choices =  (
    ('1','Active'),
    ('0','Inactive'),
    ('','Any'),
)
    classes = Classes.objects.all()

    fname = django_filters.CharFilter(field_name="fname",lookup_expr='iexact', label='First Name')
    class_id = filters.ModelChoiceFilter(queryset=classes,label='Class')
    
    status = django_filters.ChoiceFilter(choices=Status_Choices,label='Status')

    class Meta:
        model = Students
        fields = ['fname','class_id','gender','lname','status']
        exclude = ['admin','class_id', 'session_year_id','address', 'created_at', 'updated_at']