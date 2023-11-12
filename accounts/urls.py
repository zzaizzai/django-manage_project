from django.urls import path

from . import views

urlpatterns = [
    path('all_users_list', views.all_users_list, name='all_users_list'),
    path('login', views.account_login, name='account_login'),
    path('register', views.account_register, name='account_register'),
    path('account_login', views.account_logout, name='account_logout'),
]