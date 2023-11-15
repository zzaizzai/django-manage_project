from datetime import datetime
from typing import Any
from django import http
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse
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
            project.user_created = project.get_user_info(
                project.user_created_id)

        context['projects'] = all_projects
        return render(request, self.template_name, context)


class DetailProject(TemplateView):
    template_name = 'detail_project.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = super().get_context_data()
        project_id = self.kwargs['pk']
        context['project'] = Project.objects.get(id=project_id)
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
        update_proejct = Project.objects.get(id=project_id)

        update_proejct.title = context['title']
        update_proejct.text = context['text']
        update_proejct.datetime_updated= datetime.now()

        try:
            update_proejct.save()
            messages.success(request, "completely updated")
        except:
            messages.warning('failed to update')
            return render(request, self.template_name, context)

        return redirect(reverse('detail_project', kwargs={"pk": project_id}))
