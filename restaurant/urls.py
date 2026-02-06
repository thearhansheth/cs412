# File: restaurant/views.py
# Author: Arhan Sheth, 2/05/2026
# Email: aksheth@bu.edu
# Description: urls.py for Restaurant Application

from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.main_page, name='main_page'),
    path(r'main', views.main_page, name='main_page'),
    path(r'order', views.order_page, name='order_page'),
    path(r'confirmation', views.confirmation_page, name='confirmation_page')
]