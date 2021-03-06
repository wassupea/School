from django.http import request
from gms_admin.models import *
from django import forms
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget

class DateInput(forms.DateInput):
    input_type ="date"

class AddStudentForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50,widget=forms.EmailInput(attrs={"class":'form-wrapper'}))
    password =  forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(attrs={"class":'form-wrapper'}))
    fname = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={"class":'form-wrapper'}))
    lname =  forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={"class":'form-wrapper'}))
    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={"class":'form-wrapper'}))
    address = forms.CharField(label='Address', max_length=150, widget=forms.TextInput(attrs={"class":'form-wrapper'}))

    grade_level_list =[]
    try:
        gradelevels= GradeLevel.objects.all()
        
        for grade_level in gradelevels:
            small_gradelevel=(grade_level.id,grade_level.gradeLevel_no)
            grade_level_list.append(small_gradelevel)
    
    except:
        grade_level_list =[]


    session_list =[]
    try:
        sessionlists = SessionYearModel.objects.all()
        
        for session in sessionlists:
            small_sessionlist=(session.id, str(session.session_start_year)+"-"+str(session.session_end_year))
            session_list.append(small_sessionlist)
    except:
        session_list =[]


    class_list =[]
    try:
        classlist = Classes.objects.all()
        
        for classes in classlist:
            small_classlist=(classes.id, str(classes.gradelevel_id.gradeLevel_no)+"-"+str(classes.class_name))
            class_list.append(small_classlist)
    except:
        pass



    gender_choice =(
        ("Male","Male"),
        ("Female", "Female")
    )

    grade_level =  forms.ChoiceField(label='grade_level', choices=grade_level_list,widget=forms.Select(attrs={"class":'form-wrapper'}))
    class_id =  forms.ChoiceField(label='class', choices=class_list,widget=forms.Select(attrs={"class":'form-wrapper'}))
    gender = forms.ChoiceField(label='gender', choices=gender_choice,widget=forms.Select(attrs={"class":'form-wrapper'}))
    session_year_id = forms.ChoiceField(label='School Year',widget=forms.Select(attrs={"class":'form-wrapper'}), choices=session_list)



class EditStudentForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50,widget=forms.EmailInput(attrs={"class":'form-wrapper'}))
    fname = forms.CharField(label='First Name', max_length=50, widget=forms.TextInput(attrs={"class":'form-wrapper'}))
    lname =  forms.CharField(label='Last Name', max_length=50, widget=forms.TextInput(attrs={"class":'form-wrapper'}))
    username = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={"class":'form-wrapper'}))
    address = forms.CharField(label='Address', max_length=150, widget=forms.TextInput(attrs={"class":'form-wrapper'}))
    
    grade_level_list =[]
    try:
        gradelevels= GradeLevel.objects.all()
        
        for grade_level in gradelevels:
            small_gradelevel=(grade_level.id, str(grade_level.gradeLevel_no))
            grade_level_list.append(small_gradelevel)
    except:
        grade_level_list =[]


    session_list =[]
    try:
        sessionlists = SessionYearModel.objects.all()
        
        for session in sessionlists:
            small_sessionlist=(session.id, str(session.session_start_year)+"-"+str(session.session_end_year))
            session_list.append(small_sessionlist)
    except:
        pass
        #session_list =[]


    class_list =[]
    try:
        classlist = Classes.objects.all()
        
        for classes in classlist:
            small_classlist=(classes.id, str(classes.gradelevel_id_id)+"-"+str(classes.class_name))
            class_list.append(small_classlist)
    except:
        pass
        #session_list =[]

    gender_choice =(
        ("Male","Male"),
        ("Female", "Female")
    )

    grade_level =  forms.ChoiceField(label='grade_level', choices=grade_level_list,widget=forms.Select(attrs={"class":'form-wrapper'}))
    class_id =  forms.ChoiceField(label='class', choices=class_list,widget=forms.Select(attrs={"class":'form-wrapper'}))
    gender = forms.ChoiceField(label='gender', choices=gender_choice,widget=forms.Select(attrs={"class":'form-wrapper'}))
    session_year_id = forms.ChoiceField(label='School Year', choices=session_list,widget=forms.Select(attrs={"class":'form-wrapper'}))


class AddAnnouncement(forms.Form):
    subject_list =[]
    try:
        subjectlist = Subjects.objects.filter(status=1)
        
        for subject in subjectlist:
            small_subjectlist=(subject.id, str(subject.class_id_id)+"-"+str(subject.subject_name)+ "-" +str(subject.class_id.class_name))
            subject_list.append(small_subjectlist)
    except:
        pass
    subject_id =forms.ChoiceField(label='Subject', choices=subject_list,widget=forms.Select())
    title = forms.CharField(label='Title', max_length=50, widget=forms.TextInput())
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Announcements
        fields = ['subject_id', 'title', 'content']

class EditAnnouncement(forms.Form):
    subject_list =[]
    try:
        subjectlist = Subjects.objects.all()
        
        for subject in subjectlist:
            small_subjectlist=(subject.id, str(subject.class_id_id)+"-"+str(subject.subject_name))
            subject_list.append(small_subjectlist)
    except:
        pass
    subject_id =forms.ChoiceField(label='Subject', choices=subject_list,widget=forms.Select())
    title = forms.CharField(label='Title', max_length=50, widget=forms.TextInput())
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Announcements
        fields = ['subject_id', 'title', 'content']

class SendMessage(forms.Form):
    user_list = []
    try:
        users = CustomUser.objects.all()
        
        for user in users:
            small_subjectlist=(user.id, str(user.last_name)+"-"+str(user.first_name))
            user_list.append(small_subjectlist)
    except:
        pass
    user_id =forms.ChoiceField(label='Subject', choices=user_list,widget=forms.Select())
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Msg
        fields = ['user_id', 'body']

