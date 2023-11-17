from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('edit_department', EditDepartment.as_view(), name='edit_department'),
    path('add_department', AddDepartment.as_view(), name='add_department')
]