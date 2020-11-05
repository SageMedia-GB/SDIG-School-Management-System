from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from core.EmailBackEnd import EmailBackEnd


def index_page(request):
    return render(request, "index.html")


def login_page(request):
    return render(request, "login.html")


def login_action(request):
    if request.method != 'POST':
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect(reverse("headteacher_home"))
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("teacher_home"))
            elif user.user_type == "3":
                return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponse("Circuit Supervisor login"+str(user.user_type))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user is not None:
        return HttpResponse("User : " + request.user.email + " usertype : " + request.user.user_type)
    else:
        return HttpResponse("Please login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
