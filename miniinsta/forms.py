# File: miniinsta/forms.py
# Author: Arhan Sheth, 2/20/2026
# Email: aksheth@bu.edu
# Description: forms.py for Mini Insta

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """Form to add a post to the database
    """

    class Meta:
        """Associate this form with a model from our database.
        """
        model = Post
        fields = ['caption']