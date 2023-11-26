from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('all', AllOrderlist.as_view(), name='all_order_list'),
    path('detail/<str:product_name>', DetailProduct.as_view(), name='detail_product')

    
]