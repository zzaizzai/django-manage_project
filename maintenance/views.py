from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.views.generic.base import TemplateView
from maintenance.models import MasterDepartment
from django.contrib import messages
# Create your views here.

class AddDepartment(TemplateView):
    
    template_name = 'add_department.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        
        name = request.POST.get('name')
        
        new_department = MasterDepartment(name=name)
        new_department.save()
        
        return redirect('add_department')
    
    
class EditDepartment(TemplateView):
    template_name= 'edit_department.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()
        context["departments"] = MasterDepartment.objects.all().order_by('id')
        
        return render(request, self.template_name, context)
    
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        
        count_update = 0
        for department in MasterDepartment.objects.all():
            new_name = request.POST.get(f'name_{department.id}')
            if new_name is not None and new_name != department.name:
                department.name = new_name
                department.save()
                count_update += 1
        
        if count_update > 0 :
            messages.success(request, f"updated {count_update} master(s)")
            return redirect('edit_department')

        messages.warning(request, f'no one changed!')
        return redirect('edit_department')
    