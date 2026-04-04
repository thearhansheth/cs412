# File: dadjokes/views.py
# Author: Arhan Sheth, 4/03/2026
# Email: aksheth@bu.edu
# Description: views.py for dadjokes

from django.shortcuts import render, get_object_or_404
from .models import Joke, Picture
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

def random_view(request):
    """Display a random joke along with a picture
    """
    jokes = Joke.objects.all()
    pictures = Picture.objects.all()
    joke = random.choice(list(jokes))
    picture = random.choice(list(pictures))
    return render(request, 'dadjokes/random.html', {'joke': joke, 'picture': picture})

def jokes_view(request):
    """Display all jokes
    """
    jokes = Joke.objects.all()
    return render(request, 'dadjokes/jokes.html', {'jokes': jokes})

def joke_detail_view(request, pk):
    """Display a single joke using primary key
    """
    joke = get_object_or_404(Joke, pk=pk)
    return render(request, 'dadjokes/joke_detail.html', {'joke': joke})

def pictures_view(request):
    """Display all pictures
    """
    pictures = Picture.objects.all()
    return render(request, 'dadjokes/pictures.html', {'pictures': pictures})

def picture_detail_view(request, pk):
    """Display a single picture by primary key
    """
    picture = get_object_or_404(Picture, pk=pk)
    return render(request, 'dadjokes/picture_detail.html', {'picture': picture})
  
@api_view(['GET'])
def api_random_joke(request):
    """Return a random joke as JSON
    """
    jokes = Joke.objects.all()
    joke = random.choice(list(jokes))
    serializer = JokeSerializer(joke)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def api_jokes(request):
    """Return all jokes as JSON, or create a new joke
    """
    if request.method == 'GET':
        jokes = Joke.objects.all()
        serializer = JokeSerializer(jokes, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = JokeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_joke_detail(request, pk):
    """Return a single joke by primary key as JSON
    """
    joke = get_object_or_404(Joke, pk=pk)
    serializer = JokeSerializer(joke)
    return Response(serializer.data)

@api_view(['GET'])
def api_pictures(request):
    """Return all pictures as JSON
    """
    pictures = Picture.objects.all()
    serializer = PictureSerializer(pictures, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_picture_detail(request, pk):
    """Return a single picture by primary key as JSON
    """
    picture = get_object_or_404(Picture, pk=pk)
    serializer = PictureSerializer(picture)
    return Response(serializer.data)

@api_view(['GET'])
def api_random_picture(request):
    """Return a random picture as JSON
    """
    pictures = Picture.objects.all()
    picture = random.choice(list(pictures))
    serializer = PictureSerializer(picture)
    return Response(serializer.data)