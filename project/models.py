# File: project/models.py
# Author: Arhan Sheth, 4/20/2026
# Email: aksheth@bu.edu
# Description: models.py for the Job Application Tracker

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Company(models.Model):
    """Encapsulate the data of a company the user is interested in applying to.
    This is the root model. It has no foreign keys, and all other models
    relate back to it directly or indirectly.
    """

    # basic identifying information about the company
    name = models.TextField()
    industry = models.TextField()
    location = models.TextField(blank=True)

    # optional URL to the company's website for reference
    website = models.URLField(blank=True)

    # free-form notes field for any additional info the user wants to record
    notes = models.TextField(blank=True)


    def __str__(self):
        """Return a string representation of this model instance.
        """
        return f'{self.name}'


class JobPosting(models.Model):
    """Encapsulate the data of a specific job posting at a Company.
    Stores the job title, description, and the original URL of the posting
    so the user can revisit it for interview preparation.
    """

    # the company this posting belongs to
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='job_postings'
    )

    # title of the role being posted
    title = models.TextField()

    # full job description text, optional since it may be long
    description = models.TextField(blank=True)

    # the date the job was originally posted, optional
    date_posted = models.DateField(null=True, blank=True)

    # direct URL to the job posting for easy reference during interviews
    url = models.URLField(blank=True)


    def __str__(self):
        """Return a string representation of this model instance.
        """
        return f'{self.title} at {self.company.name}'


class Application(models.Model):
    """Encapsulate the data of a user's application to a specific JobPosting.
    Tracks the current pipeline stage via a status field, from Wishlist
    through to Offer or Rejected.
    """

    # choices representing each stage in the hiring pipeline
    STATUS_CHOICES = [
        ('wishlist', 'Wishlist'),
        ('applied', 'Applied'),
        ('phone_screen', 'Phone Screen'),
        ('interview', 'Interview'),
        ('final_round', 'Final Round'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]

    # the specific job posting this application is for
    job_posting = models.ForeignKey(
        JobPosting, on_delete=models.CASCADE, related_name='applications'
    )

    # the user who submitted this application
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='applications'
    )

    # the date the user submitted this application, optional for wishlist items
    date_applied = models.DateField(null=True, blank=True)

    # current pipeline stage of the application, defaults to wishlist
    status = models.TextField(choices=STATUS_CHOICES, default='wishlist')

    # free-form notes field for interview prep, recruiter info, etc.
    notes = models.TextField(blank=True)


    def __str__(self):
        """Return a string representation of this model instance.
        """
        return f'{self.user.username} -> {self.job_posting.title} ({self.get_status_display()})'
    
    @property
    def days_since_applied(self):
        """Return the number of days since this application was submitted
        """
        if not self.date_applied:
            return None
        from datetime import date
        return (date.today() - self.date_applied).days


class Contact(models.Model):
    """Encapsulate the data of a professional contact at a Company.
    Useful for tracking recruiters, hiring managers, or referrals
    associated with a specific company.
    """

    # the company this contact works at
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='contacts'
    )

    # contact's name fields
    first_name = models.TextField()
    last_name = models.TextField()

    # the contact's role or title at the company, optional
    role = models.TextField(blank=True)

    # contact's email address for outreach, optional
    email = models.EmailField(blank=True)

    # free-form notes for any additional context about this contact
    notes = models.TextField(blank=True)


    def __str__(self):
        """Return a string representation of this model instance.
        """
        return f'{self.first_name} {self.last_name} ({self.company.name})'

