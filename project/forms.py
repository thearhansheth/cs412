# File: project/forms.py
# Author: Arhan Sheth, 4/29/2026
# Email: aksheth@bu.edu
# Description: forms.py for the Job Application Tracker

from django import forms
from .models import Company, JobPosting, Application, Contact


class CompanyForm(forms.ModelForm):
    """Form for creating and updating Company records
    """
    class Meta:
        model = Company
        fields = ['name', 'industry', 'location', 'website', 'notes']


class JobPostingForm(forms.ModelForm):
    """Form for creating and updating JobPosting records
    """
    class Meta:
        model = JobPosting
        fields = ['company', 'title', 'description', 'date_posted', 'url']
        widgets = {
            # use the HTML5 date picker for the date_posted field
            'date_posted': forms.DateInput(attrs={'type': 'date'}),
        }


class ApplicationForm(forms.ModelForm):
    """Form for creating and updating Application records.
    The user FK is omitted because it is set automatically in the view
    based on the currently logged-in user.
    """
    class Meta:
        model = Application
        fields = ['job_posting', 'date_applied', 'status', 'notes']
        widgets = {
            # use the HTML5 date picker for the date_applied field
            'date_applied': forms.DateInput(attrs={'type': 'date'}),
        }


class ContactForm(forms.ModelForm):
    """Form for creating and updating Contact records
    """
    class Meta:
        model = Contact
        fields = ['company', 'first_name', 'last_name', 'role', 'email', 'notes']