from gms_admin.models import *
from django.shortcuts import redirect, render
import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from gms_admin.accounts_backend import EmailBackEnd
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import os
from django.views.generic import CreateView
from django.core.mail import send_mail
import math, random
from django.db.models.functions import Now
from gms_admin.models import Message
from django.contrib.auth.models import User
from django.template import loader, RequestContext
from django.contrib.auth.decorators import login_required
# Create your views here.
from django_otp.oath import totp
from django.utils import timezone

import datetime

def adminHome(request):
    teacher = Teacher.objects.count()
    print(teacher)
    return render (request, 'main/admin_dashboard.html', {'teacher':teacher})


def loginPage(request):
    return render(request, 'main/login2.html')

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Nah</h2>")
    else:
        #gettig user credentials from db
            otp= request.POST.get("otp")
            if OTP.objects.filter(otp=otp).exists():
                get_otp = OTP.objects.get(otp=otp)
                if get_otp.date_added < timezone.now()-timezone.timedelta(minutes=2):
                    get_otp.delete()
                    print('deleted')
                    messages.error(request,"Expired Code")
                    return HttpResponseRedirect("/login")
                
                else:  
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
                        return HttpResponseRedirect("/login")

            else:
                messages.error(request,"Invalid Credentials")
                return HttpResponseRedirect("/login")


def GetUser(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email +"usertype: " + request.user.user_type)
    else:
        return HttpResponse("Login!")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(5) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP

def otp_view(request):
    return render(request, 'main/otp.html')

def verify_otp(request):
    return render(request, 'main/verify.html')

def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email_otp')

        user = CustomUser.objects.get(email=email)
        

        if not user.is_active:
            messages.error(request, 'Inactive user')
            return HttpResponseRedirect("/")


        if CustomUser.objects.filter(email = email).filter(is_active=1).exists():
            digits = "0123456789"
            OTP2 = ""
            for i in range(4) :
                OTP2 += digits[math.floor(random.random() * 10)]
            o=OTP2
            otp = OTP(otp=o)
            otp.save()
            print(o)
            send_mail(
                        'Access Code ',
                        'Code: ' + o,
                        'hwngryjn@gmail.com',
                        [email],
                        fail_silently=False,
            )
            return HttpResponseRedirect("/login")
        else:
            messages.error(request, 'Email not existing')
            return HttpResponseRedirect("/")


def confirm_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if OTP.objects.filter(otp=otp).exists():
            return HttpResponseRedirect("/login")
        else:
            messages.error(request, 'Expired or not existing')
            return HttpResponseRedirect("verify_otp")

@login_required
def inbox(request):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct =None
    directs = None

    if messages:
        message = messages[0]
        active_direct = message['user'].last_name
        directs = Message.objects.filter(user=user, recipient=message['user'])

        for message in messages:
            if message['user'].last_name == active_direct:
                message['unread'] = 0

        context = {
            'directs': directs,
            'messages':messages,
            'active_direct':active_direct,
        }

    template = loader.get_template('teacher/chat.html')
    return HttpResponse(template.render(context, request))
