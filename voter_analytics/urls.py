# File: voter_analytics/urls.py
# Author: Arhan Sheth, 3/20/2026
# Email: aksheth@bu.edu
# Description: urls.py for Voter Analytics

from django.urls import path
from . import views

urlpatterns = [
    path('', views.VotersListView.as_view(), name='voters'),
    path('voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'),
    path('graphs', views.GraphListView.as_view(), name='graphs'),
]