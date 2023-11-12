from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import connection
# Create your views here.

def all_users_list(request):
    users = User.objects.all().order_by('id')
    return render(request, 'all_users_list.html', {"users": users})
    