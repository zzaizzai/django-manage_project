from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.views.generic.base import TemplateView
from maintenance.models import MasterDepartment
from django.contrib import messages
from manage_project.settings.database import session

from datetime import datetime
# Create your views here.

class Index(TemplateView):
    template_name='index_maintenance.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()
        
        return render(request, self.template_name, context)
    
    

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
        # context["departments"] = session.query(MasterDepartment).order_by(MasterDepartment.id.desc()).all()
        context["departments"] = MasterDepartment.get_all_master_department()
        session.close()
        return render(request, self.template_name, context)
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        
        count_update = 0
        for department in MasterDepartment.get_all_master_department():
            new_name = request.POST.get(f'name_{department.id}')
            if new_name is not None and new_name != department.name:
                department.name = new_name
                department.datetime_updated = datetime.now()
                count_update += 1
        
        session.commit()
        session.close()
        
        if count_update > 0 :
            messages.success(request, f"updated {count_update} master(s)")
            return redirect('edit_department')

        messages.warning(request, f'no one changed!')
        return redirect('edit_department')
    