# File: project/admin.py
# Author: Arhan Sheth, 4/20/2026
# Email: aksheth@bu.edu
# Description: admin.py for final project

from django.contrib import admin
from .models import Company, JobPosting, Application, Contact

# Register your models here.
admin.site.register(Company)
admin.site.register(JobPosting)
admin.site.register(Application)
admin.site.register(Contact)