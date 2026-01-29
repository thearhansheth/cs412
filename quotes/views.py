# File: quotes/views.py
# Author: Arhan Sheth, 1/29/2026
# Email: aksheth@bu.edu
# Description: views.py for Quotes Application

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
import time

tyrion_lannister_quotes = [
    "Everything's better with some wine in the belly",
    "A mind needs books as a sword needs a whetstone.",
    "Never forget who you are, for surely the world won't. Make it your strength. Then it can never be your weakness."
]

tyrion_lannister_pictures = [
    "https://upload.wikimedia.org/wikipedia/en/5/50/Tyrion_Lannister-Peter_Dinklage.jpg",
    "https://static.wikia.nocookie.net/gameofthrones/images/9/95/HandoftheKingTyrionLannister.PNG/revision/latest?cb=20190520175204",
    "https://mediaproxy.tvtropes.org/width/1200/https://static.tvtropes.org/pmwiki/pub/images/55e88dbfdd08952c388b4634_copy.jpg"
]

def quote_page(request):
    """Respond to the url 'quote.html', delegate work to a template."""
    template_name = 'quotes/quote.html'
    context = {
        "quote": tyrion_lannister_quotes[random.randint(0, len(tyrion_lannister_quotes) - 1)],
        "image": tyrion_lannister_pictures[random.randint(0, len(tyrion_lannister_pictures) - 1)],
        "time": time.ctime()
    }
    return render(request, template_name, context)

def show_all_page(request):
    """Respond to the url 'show_all.html', delegate work to a template."""
    template_name = 'quotes/show_all.html'
    context = {
        "quotes": tyrion_lannister_quotes,
        "images": tyrion_lannister_pictures,
        "time": time.ctime()
    }
    return render(request, template_name, context)

def about_page(request):
    """Respond to the url 'about_page.html', delegate work to a template."""
    template_name = 'quotes/about.html'
    context = {
        "time": time.ctime()
    }
    return render(request, template_name, context)
