from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', views.project_index, name='project_index'),
    path('add_project', AddProject.as_view(), name='add_project'),
    path('all_projects_list', AllProjectsList.as_view(), name='all_projects_list'),
    path('detail/<int:pk>', DetailProject.as_view(), name='detail_project'),
    path('edit/<int:pk>', EditProject.as_view(), name='edit_project'),
    path('add_project_member/<int:pk>', AddProjectMember.as_view(), name='add_project_member'),
    path('edit_project_member/<int:pk>', EditProjectMember.as_view(), name='edit_project_member'),
    path('create_fake', CreateFakeDate.as_view(), name='create_fake'),
    
]