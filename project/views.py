from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from .models import Project
from django.contrib.auth.models import User
from django.contrib import messages

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
        
        all_projects = Project.objects.all().order_by('-id')
        
        for project in all_projects:
            project.user_created = project.get_user_info(project.user_created_id)
            
        context['projects'] = all_projects
        return render(request, self.template_name, context)
    

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
            messages.error(request, "upload failed")
            print(e)
            return render(request, self.template_name, context)


