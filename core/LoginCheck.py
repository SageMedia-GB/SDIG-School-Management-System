from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheck(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "core.headViews":
                    pass
                elif modulename == "core.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("headteacher_home"))
            elif user.user_type == "2":
                if modulename == "core.teacherViews":
                    pass
                elif modulename == "core.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("teacher_home"))
            elif user.user_type == "3":
                if modulename == "core.studentViews":
                    pass
                elif modulename == "core.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))
        else:
            if request.path == reverse("show_login") or request.path == reverse("login"):
                pass
            else:
                return HttpResponseRedirect(reverse("login"))
