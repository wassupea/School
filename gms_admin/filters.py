from django.db.models import fields
import django_filters
from django_filters import filters

from .models import *

class TeacherFilter(django_filters.FilterSet):
    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['admin', 'gender', 'created_at', 'updated_at']

class SubjectFilter(django_filters.FilterSet):
    class Meta:
        model = Subjects
        fields = '__all__'
        exclude = ['gradelevel_id', 'created_at', 'updated_at']

class StudentFilter(django_filters.FilterSet):
    classes = Classes.objects.all()
    fname = django_filters.CharFilter(field_name="fname",lookup_expr='iexact', label='First Name')
    class_id = filters.ModelChoiceFilter(queryset=classes,label='Class')

    class Meta:
        model = Students
        fields = ['fname','class_id','gender','lname']
        exclude = ['admin','class_id', 'session_year_id','address', 'created_at', 'updated_at']