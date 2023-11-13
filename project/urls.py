from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', views.project_index, name='project_index'),
    path('add_project', AddProject.as_view(), name='add_project'),
    path('all_projects_list', AllProjectsList.as_view(), name='all_projects_list'),
]