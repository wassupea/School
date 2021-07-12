from gms_admin.models import Announcements
from django.shortcuts import render
import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from gms_admin.accounts_backend import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import os
from django.views.generic import CreateView
# Create your views here.

def adminHome(request):
    return render (request, 'main/admin_dashboard.html')

def loginPage(request):
    return render(request, 'main/login2.html')

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Nah</h2>")
    else:
        #gettig user credentials from db
        user = EmailBackEnd.authenticate(request, username= request.POST.get("email"),password = request.POST.get("password"))
        #login user
        if user!= None:
            login(request,user)
            #return HttpResponse("Email: "+request.POST.get("email") + "Password: "+ request.POST.get("password"))
            if user.user_type == '1':
                return HttpResponseRedirect('/admin_home')

            elif user.user_type =='2':
                return HttpResponseRedirect(reverse('teacher_home'))

            elif user.user_type =='3':
                return HttpResponseRedirect(reverse('student_home'))

        else:
            messages.error(request,"Invalid Credentials")
            return HttpResponseRedirect("/")

def GetUser(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email +"usertype: " + request.user.user_type)
    else:
        return HttpResponse("Login!")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


    