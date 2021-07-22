from django.db.models import fields
import django_filters

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
    class Meta:
        model = Students
        fields = '__all__'
        exclude = ['admin','class_id', 'gender', 'fname', 'address', 'created_at', 'updated_at']