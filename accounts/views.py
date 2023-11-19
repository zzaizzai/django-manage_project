from typing import Any

from django import http
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .models import CustomUser
from django.db import connection
from django.contrib import messages
from django.views.generic.base import TemplateView
from .forms import RegisterUserForm
# Create your views here.


class AllUsersList(TemplateView):
    
    template_name = 'all_users_list.html'
    
    def get(self, request, *args: Any, **kwargs: Any):
        context = self.get_context_data()
        users = CustomUser.objects.all().order_by('id')
        context['users'] = users
        return render(request, self.template_name, context)
    
    
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "logged in")
            return redirect('/')
        else:
            messages.warning(request, ("bad login method"))
            
            return redirect('/account/login')
    return render(request, 'user_login.html')


def user_register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("core_index")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")

    form = RegisterUserForm()
    return render(request, 'user_register.html', {"form": form})


class UserLogout(TemplateView):

    def get(self, request, *args: Any, **kwargs: Any):
        logout(request)
        return redirect(reverse_lazy('user_login'))


class MyPage(TemplateView):
    template_name = 'mypage.html'
    def get(self, request, *args: Any, **kwargs: Any):
        context = self.get_context_data()
        
        user = request.user
        context['user'] = CustomUser.objects.get(id=user.id)
        
        return render(request, self.template_name, context)


class DetailUser(TemplateView):
    template_name = 'detail_user.html'
    
    def get(self, request, *args: Any, **kwargs: Any):
        context = super().get_context_data()
        user_id = self.kwargs['pk']
        
        try:
            user = CustomUser.objects.get(id=user_id)
            context['user'] = user
        except:
            return redirect('all_users_list')
        
        return render(request, self.template_name, context)
    