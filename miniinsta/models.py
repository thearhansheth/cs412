# File: miniinsta/models.py
# Author: Arhan Sheth, 2/13/2026
# Email: aksheth@bu.edu
# Description: models.py for Mini Insta

from django.db import models

# Create your models here.
class Profile(models.Model):
    """Encapsulate the data of an insta Profile.
    """

    # define the data attributes of the article object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        """Return a string representation of this model instance.
        """
        return f'{self.username}: {self.display_name}'