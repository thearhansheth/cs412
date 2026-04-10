# File: miniinsta/views.py
# Author: Arhan Sheth, 2/13/2026
# Email: aksheth@bu.edu
# Description: views.py for Mini Insta


from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from miniinsta.forms import *
from .models import *
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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

    def get_context_data(self, **kwargs):
        """Override get_context_data to add profile to context for footer
        """
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['profile'] = Profile.objects.filter(user=self.request.user).first()

        return context

class CreatePostView(LoginRequiredMixin, CreateView):
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
        context["profile"] = Profile.objects.get(user=self.request.user)
        return context
    
    def form_valid(self, form):
        """validate incoming create post form
        """
        profile = Profile.objects.get(user=self.request.user)
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
    
    def get_object(self):
        """Return one instance of the Profile object
        """
        return Profile.objects.get(user=self.request.user)
    
    def get_login_url(self):
        """Return the url for this app's login page
        """
        return reverse('login')
    

class UpdateProfileView(UpdateView):
    """View to handle the update of a profile
    """
    model = Profile
    form_class = UpdateProfileForm
    template_name = "miniinsta/update_profile_form.html"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
    def get_success_url(self):
        # redirect to the updated profile page
        return reverse("show_my_profile")
    
    def get_login_url(self):
        """Return the url for this app's login page
        """
        return reverse('login')

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
    

class UpdatePostView(LoginRequiredMixin, UpdateView):
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


class PostFeedListView(LoginRequiredMixin, ListView):
    """View to handle displaying the post feed of a given profile
    """
    model = Post
    template_name = "miniinsta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Return the posts in the feed for this profile
        """
        profile = Profile.objects.get(user=self.request.user)
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        """Add the current profile to the context
        """
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context
    
    def get_login_url(self):
        """Return the url for this app's login page
        """
        return reverse('login')


class SearchView(LoginRequiredMixin, ListView):
    """View to handle searching for profiles and posts
    """
    model = Profile
    template_name = "miniinsta/search_results.html"
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):
        """Render template form if no query form, otherwise return dispatch
        """
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if "q" not in self.request.GET:
            profile = Profile.objects.get(user=self.request.user)
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
        profile = Profile.objects.get(user=self.request.user)
        posts = self.get_queryset()
        matching_profiles = Profile.objects.filter(username__icontains=query) | \
                            Profile.objects.filter(display_name__icontains=query) | \
                            Profile.objects.filter(bio_text__icontains=query)
        context["profile"] = profile
        context["query"] = query
        context["posts"] = posts
        context["profiles"] = matching_profiles
        return context
    
    def get_login_url(self):
        """Return the url for this app's login page
        """
        return reverse('login')
    
class MyProfileDetailView(LoginRequiredMixin, DetailView):
    """Display the logged-in user's own profile
    """
    model = Profile
    template_name = "miniinsta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        """Return the profile of the logged-in user
        """
        return Profile.objects.get(user=self.request.user)


class CreateProfileView(CreateView):
    """View for handling creating a profile
    """
    model = Profile
    template_name = "miniinsta/create_profile_form.html"
    fields = ['username', 'display_name', 'profile_image_url', 'bio_text']

    def get_context_data(self, **kwargs):
        """Override the built in get_context_data to populate fields
        """
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        """Validate incoming create profile form
        """
        user_form = UserCreationForm(self.request.POST)

        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user
            return super().form_valid(form)
        else:
            context = self.get_context_data(form=form)
            context['user_form'] = user_form
            return self.render_to_response(context)
    
    def get_success_url(self):
        """Redirect to the Profile's detail page
        """
        return reverse('show_my_profile')


class CreateFollowView(LoginRequiredMixin, CreateView):
    """View for handling a profile following another profile
    """
    model = Follow
    form_class = CreateFollowForm
    template_name = "miniiinsta/follow_form.html"

    def get_login_url(self):
        """Return the url for this app's login page
        """
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        """Override the built in get_context_data to populate fields
        """
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs["pk"])
        context["follower_profile"] = Profile.objects.get(user=self.request.user)
        return context
    
    def form_valid(self, form):
        """Set the follower and followed profiles before saving
        """
        form.instance.profile = Profile.objects.get(pk=self.kwargs["pk"])
        form.instance.follower_profile = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the followed profile's detail page
        """
        return reverse("show_profile", kwargs={"pk": self.object.profile.pk})
    

class DeleteFollowView(LoginRequiredMixin, DeleteView):
    """View to handle the deletion of a follow relationship
    """
    model = Follow
    template_name = "miniinsta/delete_follow_form.html"
    form_class = DeleteFollowForm

    def get_login_url(self):
        """Return the url for this app's login page
        """
        return reverse('login')
    
    def get_object(self, queryset=None):
        """Return the follow object between the current user and target profile
        """
        profile_to_unfollow = Profile.objects.get(pk=self.kwargs["pk"])
        follower_profile = Profile.objects.get(user=self.request.user)
        return Follow.objects.get(profile=profile_to_unfollow, follower_profile=follower_profile)
    
    def get_context_data(self, **kwargs):
        """Override the built in get_context_data to populate fields
        """
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=self.kwargs["pk"])
        context["follower_profile"] = Profile.objects.get(user=self.request.user)
        return context
    
    def get_success_url(self):
        """Redirect to the unfollowed profile's detail page
        """
        return reverse("show_profile", kwargs={"pk": self.object.profile.pk})
    
class LikeDetailView(LoginRequiredMixin, CreateView):
    """View to handle liking a post
    """
    model = Like

    def get_login_url(self):
        """Return the url for this app's login page
        """
        return reverse('login')
    
    def post(self, request, *args, **kwargs):
        """Create a like object if the user is not liking their own post
        """
        post = Post.objects.get(pk=self.kwargs["pk"])
        profile = Profile.objects.get(user=request.user)

        if post.profile != profile:
            Like.objects.get_or_create(post=post, profile=profile)

        return redirect("show_post", pk=post.pk)
class LikeDeleteView(LoginRequiredMixin, DeleteView):
    """View to handle unliking a post
    """
    model = Like

    def get_login_url(self):
        """Return the url for this app's login page
        """
        return reverse('login')
    
    def post(self, request, *args, **kwargs):
        """Delete the like object if it exists
        """
        post = Post.objects.get(pk=self.kwargs["pk"])
        profile = Profile.objects.get(user=request.user)
        like = Like.objects.filter(post=post, profile=profile).first()

        if like:
            like.delete()
            
        return redirect("show_post", pk=post.pk)

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user registration.
    Write-only field for password
    """
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']
    def create(self, validated_data):
        """Used create_user so the password gets hashed properly.
        """
        return User.objects.create_user(**validated_data)
    
class UserRegistrationView(CreateAPIView):
    """POST /api/register/ - create a new user account
    """
    serializer_class = UserSerializer
    
class LoginAPIView(APIView):
    """POST /api/login/ - authenticate and return token + profile_id
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        """Step 1 of login: client fetches a CSRF token first"""
        from django.middleware.csrf import get_token
        return Response({'csrfToken': get_token(request)})
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        token, _ = Token.objects.get_or_create(user=user)
        profile = Profile.objects.filter(user=user).first()

        return Response({
            'token': token.key,
            'profile_id': profile.pk if profile else None,
        })
class ProfileListAPIView(APIView):
    """GET /api/profiles/ - list all profiles
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        profiles = Profile.objects.all()
        data = [
            {
                'id': p.pk,
                'username': p.username,
                'display_name': p.display_name,
                'profile_image_url': p.profile_image_url,
                'bio_text': p.bio_text,
            }
            for p in profiles
        ]

        return Response(data)
    
class ProfileDetailAPIView(APIView):
    """GET /api/profiles/<pk>/ -single profile + their posts
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        posts = [
            {
                'id': post.pk,
                'caption': post.caption,
                'timestamp': post.timestamp,
                'photos': [p.get_image_url() for p in post.get_all_photos()],
            }
            for post in profile.get_all_posts()
        ]

        return Response({
            'id': profile.pk,
            'username': profile.username,
            'display_name': profile.display_name,
            'profile_image_url': profile.profile_image_url,
            'bio_text': profile.bio_text,
            'posts': posts,
        })
        
class FeedAPIView(APIView):
    """GET /api/profiles/<pk>/feed/ - feed for a profile
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            profile = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        
        posts = [
            {
                'id': post.pk,
                'caption': post.caption,
                'timestamp': post.timestamp,
                'profile_id': post.profile.pk,
                'username': post.profile.username,
                'profile_image_url': post.profile.profile_image_url,
                'photos': [p.get_image_url() for p in post.get_all_photos()],
            }
            for post in profile.get_post_feed()
        ]

        return Response(posts)
    
class CreatePostAPIView(APIView):
    """POST /api/posts/ - create a new post, owner set from token
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        profile = Profile.objects.filter(user=request.user).first()

        if not profile:
            return Response({'error': 'No profile found'}, status=status.HTTP_400_BAD_REQUEST)
        
        caption = request.data.get('caption', '')
        image_url = request.data.get('image_url', '')
        post = Post.objects.create(profile=profile, caption=caption)

        if image_url:
            Photo.objects.create(post=post, image_url=image_url)

        return Response({
            'id': post.pk,
            'caption': post.caption,
            'timestamp': post.timestamp,
            'profile_id': profile.pk,
        }, 
        status=status.HTTP_201_CREATED)