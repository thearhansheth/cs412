# File: miniinsta/views.py
# Author: Arhan Sheth, 2/13/2026
# Email: aksheth@bu.edu
# Description: views.py for Mini Insta


from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from miniinsta.forms import CreatePostForm
from .models import *
# Create your views here.

class ProfileListView(ListView):
    """View to display all profiles"""
    model = Profile
    template_name = 'miniinsta/show_all_profiles.html'
    context_object_name = 'profiles'
    
class ProfileDetailView(DetailView):
    """Display a single profile
    """

    model = Profile
    template_name = "miniinsta/show_profile.html"
    context_object_name = "profile"


class PostDetailView(DetailView):
    """Display a single post
    """

    model = Post
    template_name = "miniinsta/show_post.html"
    context_object_name = "post" 

class CreatePostView(CreateView):
    """A view to handle creation of a new Post
        --> Display the html form to the user (GET)
        --> Process form submission and store the new post object (POST)
    """

    form_class = CreatePostForm
    template_name = "miniinsta/create_post_form.html"
    
    def get_context_data(self, **kwargs):
        """override the built in get_context_data to populate fields
        """
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        """validate incoming create post form
        """
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        image_url = self.request.POST.get('image_url')
        post = form.save()
        if image_url:
            Photo.objects.create(post=post, image_url=image_url)
        return super().form_valid(form)
        
        
    def get_success_url(self):
        """redirect to the new Post’s detail page
        """
        return reverse("show_post", kwargs={"pk": self.object.pk})
