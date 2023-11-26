import os
from typing import Any
from datetime import datetime

from django import http
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from .models import Order, Product


# Create your views here.
class AllOrderlist(TemplateView):
    
    template_name = 'all_order_list.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()
        
        path = os.path.join(settings.BASE_DIR, 'sample_data\data1.csv')
        
        orders = Order.get_orders_from_csv(path)
        context['orders'] = orders
        
        return render(request, self.template_name, context) 
    
class DetailProduct(TemplateView):
    
    template_name='detail_product.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()
        product_name =  self.kwargs['product_name']
        product = Product(name=product_name)
        context['product'] = product
        
        print(product.get_orders())
        return render(request, self.template_name, context) 