from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages


def index(request):
    myapp_data = {
    'app': 'Django'
    }
    
    messages.success(request, "alert test")
    return render(request, 'core_index.html', myapp_data)