from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    myapp_data = {
    'app': 'Django'
    }
    return render(request, 'core_index.html', myapp_data)