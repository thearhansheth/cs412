# File: dadjokes/admin.py
# Author: Arhan Sheth, 4/03/2026
# Email: aksheth@bu.edu
# Description: admin.py for dadjokes

from django.contrib import admin

# Register your models here.
from .models import Joke, Picture
admin.site.register(Joke)
admin.site.register(Picture)
