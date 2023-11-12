from django.urls import path

from . import views

urlpatterns = [
    path('all_users_list', views.all_users_list, name='all_users_list'),
]