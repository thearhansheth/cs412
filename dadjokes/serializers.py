# File: dadjokes/serializers.py
# Author: Arhan Sheth, 4/03/2026
# Email: aksheth@bu.edu
# Description: serializers.py for dadjokes

from rest_framework import serializers
from .models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):
    '''serialize a Joke object to JSON'''
    class Meta:
        model = Joke
        fields = ['id', 'text', 'name', 'timestamp']

class PictureSerializer(serializers.ModelSerializer):
    '''serialize a Picture object to JSON'''
    class Meta:
        model = Picture
        fields = ['id', 'picture', 'name', 'timestamp']