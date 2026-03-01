# File: miniinsta/views.py
# Author: Arhan Sheth, 2/13/2026
# Email: aksheth@bu.edu
# Description: views.py for Mini Insta


from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from miniinsta.forms import *
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
    

class UpdateProfileView(UpdateView):
    """View to handle the update of a profile
    """
    model = Profile
    form_class = UpdateProfileForm
    template_name = "miniinsta/update_profile_form.html"
    
    def get_success_url(self):
        # redirect to the updated profile page
        return reverse("show_profile", kwargs={"pk": self.object.pk})
    

class DeletePostView(DeleteView):
    """View to handle the deletion of a post
    """
    model = Post
    template_name = "miniinsta/delete_post_form.html"

    def get_context_data(self,  **kwargs):
        """Override the built in get_context_data to populate fields
        """
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        profile = post.profile
        context['post'] = post
        context['profile'] = profile
        return context
    
    def get_success_url(self):
        """Redirect to the deleted post's corresponding profile detail page
        """
        return reverse("show_profile", kwargs={"pk": self.object.profile.pk})
    

class UpdatePostView(UpdateView):
    """View to handle updating a post
    """
    model = Post
    form_class = UpdatePostForm
    template_name = "miniinsta/update_post_form.html"

    def get_context_data(self,  **kwargs):
        """Override the built in get_context_data to populate fields
        """
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        profile = post.profile
        caption = post.caption
        context['post'] = post
        context['caption'] = caption
        context['profile'] = profile
        return context
    
    def get_success_url(self):
        """Redirect to the updated post's detail page
        """
        return reverse("show_post", kwargs={"pk": self.object.pk})
    

class ShowFollowersDetailView(DetailView):
    """View to handle displaying followers
    """
    model = Profile
    template_name = "miniinsta/show_followers.html"
    context_object_name = "profile"

    def get_context_data(self,  **kwargs):
        """Override the built in get_context_data to populate fields
        """
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['followers'] = profile.get_followers()
        context['num_followers'] = profile.get_num_followers()
        return context


class ShowFollowingDetailView(DetailView):
    """View to handle displaying following
    """
    model = Profile
    template_name = "miniinsta/show_following.html"
    context_object_name = "profile"

    def get_context_data(self,  **kwargs):
        """Override the built in get_context_data to populate fields
        """
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context["following"] = profile.get_following()
        context["num_following"] = profile.get_num_following()
        return context


class PostFeedListView(ListView):
    """View to handle displaying the post feed of a given profile
    """
    model = Post
    template_name = "miniinsta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Return the posts in the feed for this profile
        """
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        """Add the current profile to the context
        """
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context


class SearchView(ListView):
    """View to handle searching for profiles and posts
    """
    model = Profile
    template_name = "miniinsta/search_results.html"
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):
        """Render template form if no query form, otherwise return dispatch
        """
        if "q" not in self.request.GET:
            profile = Profile.objects.get(pk=self.kwargs['pk'])
            return render(request, "miniinsta/search.html", {"profile": profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Return posts which match the query
        """
        query = self.request.GET.get("q")
        if query:
            return Post.objects.filter(caption__icontains=query)
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        """Add profile, query, posts, and matching profiles to context
        """
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        posts = self.get_queryset()
        matching_profiles = Profile.objects.filter(username__icontains=query) | \
                            Profile.objects.filter(display_name__icontains=query) | \
                            Profile.objects.filter(bio_text__icontains=query)
        context["profile"] = profile
        context["query"] = query
        context["posts"] = posts
        context["profiles"] = matching_profiles
        return context