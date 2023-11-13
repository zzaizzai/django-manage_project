from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import connection
from django.contrib import messages

from .forms import RegisterUserForm
# Create your views here.

def all_users_list(request):
    users = User.objects.all().order_by('id')
    return render(request, 'all_users_list.html', {"users": users})
    
def account_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "logged in")
            return redirect('/')

        else:
            messages.success(request, ("bad login method"))
            
            return redirect('/members/login_user')
    return render(request, 'account_login.html')

def account_register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("account_login")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")

    form = RegisterUserForm()
    return render(request, 'account_register.html', {"form": form})


def account_logout(request):
    logout(request)
    messages.success(request, ("logged out"))

    return redirect('account_login')


def mypage(request):
    
    return render(request, 'mypage.html')