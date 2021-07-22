from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "gms_admin.adminViews":
                    pass
                elif modulename == "gms_admin.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "gms_admin.teacherViews":
                    pass
                elif modulename == "gms_admin.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("teacher_home"))
            elif user.user_type == "3":
                if modulename == "gms_admin.studentViews":
                    pass
                elif modulename == "gms_admin.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse("do_login") or request.path == reverse("send_otp") or modulename == "django.contrib.auth.views":
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))