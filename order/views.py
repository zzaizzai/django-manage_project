from datetime import datetime
from typing import Any
import os
from django import http
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Order
from django.conf import settings

# Create your views here.
class AllOrderlist(TemplateView):
    
    template_name = 'all_order_list.html'
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = self.get_context_data()
        
        path = os.path.join(settings.BASE_DIR, 'sample_data\data1.csv')
        
        orders = Order.get_orders_from_csv(path)
        context['orders'] = orders
        
        return render(request, self.template_name, context) 
    
    