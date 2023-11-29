from datetime import datetime, timedelta
from typing import Any

from django.utils import timezone
from django import http
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from core.models import Project, CustomUser, ProjectMember
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from manage_project.settings.database import session
# from accounts.models import CustomUser
from .models import  ProjectComment


def project_index(request):
    myapp_data = {
        'app': 'Django'
    }
    return render(request, 'project_index.html', myapp_data)


class AllProjectsList(TemplateView):
    template_name = 'all_projects_list.html'
    paginate_by = 15
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        
        
        search_word = request.GET.get('q')
        sort = request.GET.get('sort')
        page = request.GET.get('page')
        context['sort'] = sort if sort else ""
        context['q'] = search_word if search_word else ""
        context['page'] = page if page else ""
        
        # Retrieve all projects
        if search_word is None or len(search_word) == 0:
            projects = Project.get_projects_with_options(search_word, sort)
        else:
            projects = Project.get_projects_with_options(search_word, sort)
            
            
        #* DEMO projects
        days_ago = datetime.now(timezone.utc) - timedelta(days=100)
        aa = Project.get_demo_proejct(datetime_created=days_ago)
        days_ago = datetime.now(timezone.utc) - timedelta(days=999)
        bb  = Project.get_demo_proejct(datetime_created=days_ago)
        projects.append(aa)
        projects.append(bb)
        
        
        # Paginate the projects
        paginator = Paginator(projects, self.paginate_by)
        try:
            projects = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver the first page.
            projects = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver the last page of results.
            projects = paginator.page(paginator.num_pages)
            
            

        
        
        context['projects'] = projects
        session.close()
        
        return render(request, self.template_name, context)


class DetailProject(TemplateView):
    template_name = 'detail_project.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = super().get_context_data()
        project_id = self.kwargs['pk']
        
        
        project = Project.get_project(project_id=project_id)
        session.close()

        if project is None:
            messages.warning(request, "project page error")
            return redirect('all_projects_list')
        
        context['project'] = project
        return render(request, self.template_name, context)
    
    # Create Comment
    def post(self, request, *args, **kwargs):
        project_id = self.kwargs['pk']
        comment_text = request.POST.get('comment-text')
        try:
            ProjectComment.create_comment(request.user.id, project_id, comment_text)
            messages.success(request, "added a comment")
        except:
            messages.warning(request, "failed to save comment")
        return redirect(reverse('detail_project', kwargs={"pk": project_id}))
    

class EditProjectMember(TemplateView):
    
    template_name = 'edit_project_member.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()
        project_id = self.kwargs['pk']
        # projects =  Project.objects.get(id=project_id)
        project = session.query(Project).filter_by(id=project_id).first()
        
        exclude_ids = [member.user_id for member in project.get_members()]
        users = session.query(CustomUser).filter(~CustomUser.id.in_(exclude_ids)).order_by(CustomUser.id).all()
        
        context['users'] = users
        context['project'] = project
        
        session.close()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        
        project_id = self.kwargs['pk']
        project = session.query(Project).filter_by(id=project_id).first()
        
        members = project.get_members()
        print(members)
        is_changed, is_errored = False, False

        try:
            for member in members:
                change_to = request.POST.get(f'manager_{member.user_id}') or False 
                change_from = member.is_manager
                
                if bool(change_to) is not change_from:
                    member.is_manager = bool(change_to)
                    is_changed = True
                    
            session.commit() 
        except Exception as e:
            session.rollback()  
            is_errored = True
            print(f"Error during commit: {e}")
        finally:
            session.close()
                    
        if is_changed:
            messages.success(request, "update done")
            
        if is_errored:
            messages.warning(request, "failed to update")
        
        session.close()
        return redirect(reverse('detail_project', kwargs={"pk": project_id}))
    
class AddProjectMember(TemplateView):
    template_name = 'add_project_member.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()
        
        project_id = self.kwargs['pk']
        context['project'] = Project.get_project(project_id=project_id)
        context['users'] = CustomUser.get_all_users()
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['user_id'] = request.POST.get('user_id')
        context['project_id'] = self.kwargs['pk']
        
        try:
            project_member = session.query(ProjectMember).filter_by(user_id=context['user_id'], project_id=context['project_id']).first()
        except ProjectMember.DoesNotExist:
            project_member = None
            
        #* if already the users exist, go back to page 
        if project_member is not None:
            messages.warning(request , "user is already member")
            return redirect(reverse('detail_project', kwargs={"pk": context['project_id']}))
        
        try:
            user = CustomUser.get_user(user_id=context['user_id'])
            new_project_memeber = ProjectMember(user_id=user.id, project_id = context['project_id'])
            session.add(new_project_memeber)
            session.commit()
            messages.success(request, "done!")
        except:
            session.rollback()
            messages.warning(request, "failed to add member")
        finally:
            session.close()
            
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
        
        new_project = Project(
            title=context['title'],
            text=context['text'],
            user_created_id=request.user.id
        )
        
        is_success = False
        try:
            session.add(new_project)
            session.commit()
            messages.success(request, "upload done")
            is_success = True
        except Exception as e:
            session.rollback()
            messages.warning(request, f"upload failed {e}")
        finally:
            session.close()
            
        if is_success is True:
            return redirect('project_index')
        
        return render(request, self.template_name, context)
        

class EditProject(TemplateView):
    template_name = 'edit_project.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['pk']

        try:
            context['project'] = Project.get_project(project_id=project_id)
        except Exception as e:
            print(e)
        finally:
            session.close()
            
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
        context['is_completed'] = bool(request.POST.get('is_completed', False) )
        context['is_canceled'] = bool(request.POST.get('is_canceled', False)) 
        context['date_due'] = request.POST.get('date_due') or None 
        
        update_proejct = Project.get_project(project_id=project_id)
        update_proejct.title = context['title']
        update_proejct.text = context['text']
        update_proejct.is_completed = bool(context['is_completed'])
        update_proejct.is_canceled = bool(context['is_canceled'])
        update_proejct.datetime_updated= datetime.now()
        update_proejct.date_due = context['date_due']
        
        
        try:
            session.commit()
            messages.success(request, "completely updated")
        except Exception as e:
            session.rollback()
            messages.warning(request, f"failed to update: {e}")
            return render(request, self.template_name, context)
        finally:
            session.close()
            
        return redirect(reverse('detail_project', kwargs={"pk": project_id}))


class CreateFakeDate(TemplateView):

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        from faker import Faker
        import random
        
        fake = Faker()
        
        business_sentence_1 = fake.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None)
        business_sentence_2 = fake.sentence(nb_words=8, variable_nb_words=True, ext_word_list=None)
        business_sentence_3 = fake.sentence(nb_words=12, variable_nb_words=True, ext_word_list=None)

        # 3줄 합치기
        combined_business_sentences = f"{business_sentence_1} {business_sentence_2} {business_sentence_3}"
        
        start_date = datetime.strptime('2022-01-01', '%Y-%m-%d')
        end_date = datetime.strptime('2022-12-31', '%Y-%m-%d')

        random_date = fake.date_between(start_date=start_date, end_date=end_date)
        due_date = random_date + timedelta(days=random.randint(10, 60))
        
        fake_data = {
            'name': fake.name(),
            'user_created_id' : random.randint(1,4),
            'address': fake.address(),
            'email': fake.email(),
            'text': fake.text(),
            'word': fake.word(),
            'random_date': random_date,
            'due_date': due_date,
            'business_sentence ': fake.sentence(nb_words=10, variable_nb_words=True, ext_word_list=None),
            'combined_business_sentences': combined_business_sentences
        }
        return JsonResponse(fake_data)
    