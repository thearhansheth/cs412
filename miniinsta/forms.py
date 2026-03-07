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


class UpdateProfileForm(forms.ModelForm):
    """Form to update a profile in the database
    """

    class Meta:
        """Associate this form with a model from our database
        """
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']
        
class UpdatePostForm(forms.ModelForm):
    """Form to update a post in the database
    """

    class Meta:
        """Associate this form with a model from our database
        """
        model = Post
        fields = ['caption']

class CreateProfileForm(forms.ModelForm):
    """Dorm to create a profile
    """

    class Meta:
        """Assocate this form with a model from our database
        """
        model = Profile
        fields = ['username', 'display_name', 'bio_text', 'profile_image_url']
        
class CreateFollowForm(forms.ModelForm):
    """Form to create a follow relationship between two profile objects
    """

    class Meta:
        """Associate this form with a model from our database
        """
        model = Follow
        fields = []

class DeleteFollowForm(forms.ModelForm):
    """Form to delete a follow relationship between two profile objects
    """

    class Meta:
        """Associate this form with a model from our database
        """
        model = Follow
        fields = []