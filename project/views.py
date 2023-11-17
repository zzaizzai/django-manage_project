from datetime import datetime
from typing import Any

from django import http
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages

from accounts.models import CustomUser
from .models import Project, ProjectMemeber


def project_index(request):
    myapp_data = {
        'app': 'Django'
    }
    return render(request, 'project_index.html', myapp_data)


class AllProjectsList(TemplateView):
    template_name = 'all_projects_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        context['projects'] = Project.objects.all().order_by('-id')

        return render(request, self.template_name, context)


class DetailProject(TemplateView):
    template_name = 'detail_project.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = super().get_context_data()
        project_id = self.kwargs['pk']
        context['project'] = Project.objects.get(id=project_id)
        return render(request, self.template_name, context)

class AddProjectMember(TemplateView):
    template_name = 'add_project_member.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()
        
        project_id = self.kwargs['pk']
        context['project'] = Project.objects.get(id=project_id)
        context['users'] = CustomUser.objects.all().order_by('id')
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['user_id'] = request.POST.get('user_id')
        context['project_id'] = self.kwargs['pk']
        
        try:
            project_member = ProjectMemeber.objects.get(user_id = context['user_id'], project_id = context['project_id'])
        except ProjectMemeber.DoesNotExist:
            project_member = None
            
        if project_member is not None:
            messages.warning(request , "user is already member")
            return redirect(reverse('detail_project', kwargs={"pk": context['project_id']}))
        
        try:
            user = CustomUser.objects.get(id=context['user_id'])
            new_project_memeber = ProjectMemeber(user_id=user.id, project_id = context['project_id'])
            new_project_memeber.save()
            messages.success(request, "done!")
        except:
            messages.warning(request, "failed to add member")
            
        return redirect(reverse('detail_project', kwargs={"pk": context['project_id']}))

        
class AddProject(TemplateView):
    template_name = 'add_project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        context['title'] = request.POST.get('title')
        context['text'] = request.POST.get('text')
        print()
        new_project = Project(
            title=context['title'],
            text=context['text'],
            user_created_id=request.user.id
        )
        try:
            new_project.save()
            messages.success(request, "upload done")
            return redirect('project_index')
        except Exception as e:
            messages.warning(request, "upload failed")
            print(e)
            return render(request, self.template_name, context)


class EditProject(TemplateView):
    template_name = 'edit_project.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['pk']

        try:
            context['project'] = Project.objects.get(id=project_id)
        except:
            pass

        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()

        if 'project' not in context:
            return redirect('all_projects_list')

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        project_id = request.POST.get('id')

        context['title'] = request.POST.get('title')
        context['text'] = request.POST.get('text')
        context['is_completed'] = request.POST.get('is_completed', False) 
        context['is_cancled'] = request.POST.get('is_cancled', False) 
        
        update_proejct = Project.objects.get(id=project_id)

        update_proejct.title = context['title']
        update_proejct.text = context['text']
        update_proejct.is_completed = context['is_completed']
        update_proejct.is_cancled = context['is_cancled']
        update_proejct.datetime_updated= datetime.now()
        print(context['is_completed'])
        print(context['is_cancled'])
        try:
            update_proejct.save()
            messages.success(request, "completely updated")
        except:
            messages.warning( request, 'failed to update')
            return render(request, self.template_name, context)

        return redirect(reverse('detail_project', kwargs={"pk": project_id}))
