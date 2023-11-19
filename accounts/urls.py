from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('all', AllUsersList.as_view(), name='all_user_list'),
    path('login', views.user_login, name='user_login'),
    path('register', views.user_register, name='user_register'),
    path('logout', UserLogout.as_view(), name='user_logout'),
    path('mypage', MyPage.as_view(), name='mypage'),
    path('detail/<int:pk>', DetailUser.as_view(), name='detail_user' )
]