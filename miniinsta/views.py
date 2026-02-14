# File: miniinsta/views.py
# Author: Arhan Sheth, 2/13/2026
# Email: aksheth@bu.edu
# Description: views.py for Mini Insta


from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile
# Create your views here.

class ProfileListView(ListView):
    """View to display all profiles"""
    model = Profile
    template_name = 'miniinsta/show_all_profiles.html'
    context_object_name = 'profiles'
    
class ProfileDetailView(DetailView):
    '''Display a single profile.'''

    model = Profile
    template_name = "miniinsta/show_profile.html"
    context_object_name = "profile" # note singular variable name