from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from .models import CustomUser
from manage_project.settings.database import session

def index(request):
    myapp_data = {
    'app': 'Django'
    }
    oo = session.query(CustomUser).all()
    print(oo)
    
    messages.success(request, "alert test")
    return render(request, 'core_index.html', myapp_data)