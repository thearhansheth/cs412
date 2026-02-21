# File: miniinsta/urls.py
# Author: Arhan Sheth, 2/13/2026
# Email: aksheth@bu.edu
# Description: urls.py for Mini Insta


from django.urls import path
from .views import *

urlpatterns = [
    path(r'', ProfileListView.as_view(), name="show_all_profiles"),
    path(r'show_all_profiles', ProfileListView.as_view(), name="show_all_profiles"),
    path(r'profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='show_post'),
    path(r'profile/<int:pk>/create_post', CreatePostView.as_view(), name="create_post"),
]