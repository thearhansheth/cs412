# File: project/urls.py
# Author: Arhan Sheth, 4/20/2026
# Email: aksheth@bu.edu
# Description: urls.py for the Job Application Tracker

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
 
urlpatterns = [
    # main dashboard, the landing page after login
    path('', views.dashboard_view, name='dashboard'),

    # authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup'),

    # Company CRUD URLs
    path('companies/', views.CompanyListView.as_view(), name='company_list'),
    path('companies/<int:pk>/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('companies/create/', views.CompanyCreateView.as_view(), name='company_create'),
    path('companies/<int:pk>/update/', views.CompanyUpdateView.as_view(), name='company_update'),
    path('companies/<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='company_delete'),

    # JobPosting CRUD URLs
    path('job-postings/', views.JobPostingListView.as_view(), name='job_posting_list'),
    path('job-postings/<int:pk>/', views.JobPostingDetailView.as_view(), name='job_posting_detail'),
    path('job-postings/create/', views.JobPostingCreateView.as_view(), name='job_posting_create'),
    path('job-postings/<int:pk>/update/', views.JobPostingUpdateView.as_view(), name='job_posting_update'),
    path('job-postings/<int:pk>/delete/', views.JobPostingDeleteView.as_view(), name='job_posting_delete'),
 
    # Application CRUD URLs
    path('applications/', views.ApplicationListView.as_view(), name='application_list'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('applications/create/', views.ApplicationCreateView.as_view(), name='application_create'),
    path('applications/<int:pk>/update/', views.ApplicationUpdateView.as_view(), name='application_update'),
    path('applications/<int:pk>/delete/', views.ApplicationDeleteView.as_view(), name='application_delete'),
    
    # Contact CRUD URLs
    path('contacts/', views.ContactListView.as_view(), name='contact_list'),
    path('contacts/<int:pk>/', views.ContactDetailView.as_view(), name='contact_detail'),
    path('contacts/create/', views.ContactCreateView.as_view(), name='contact_create'),
    path('contacts/<int:pk>/update/', views.ContactUpdateView.as_view(), name='contact_update'),
    path('contacts/<int:pk>/delete/', views.ContactDeleteView.as_view(), name='contact_delete'),
]