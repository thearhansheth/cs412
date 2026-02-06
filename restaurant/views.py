# File: restaurant/views.py
# Author: Arhan Sheth, 2/05/2026
# Email: aksheth@bu.edu
# Description: views.py for Restaurant Application

from django.http import HttpResponse
from django.shortcuts import render
import random
import time
from datetime import datetime, timedelta

entree_prices = {
    "Fried Rice $12": 12,
    "Noodles $10": 10,
    "Steamed Veggies $10": 10,
    "A La Carte Bowl $15": 15,
    "Chicken $3": 3
}

specials = ["Wontons $5", "Veggie Spring Rolls $5", "Chicken Rolls $5"]
special_of_the_day = specials[random.randint(0, len(specials) - 1)]

def main_page(request):
    """Respond to the url 'main.html' and '', delegate work to a template.
    """
    template_name = 'restaurant/main.html'
    context = {
        "time": time.ctime(),
        "picture_link": "nud-pob.webp"
    }
    return render(request, template_name, context)

def order_page(request):
    """Respond to the url 'order.html', delegate work to a template.
    """
    template_name = 'restaurant/order.html'
    context = {
        "time": time.ctime(),
        "special": special_of_the_day
    }
    return render(request, template_name, context)

def confirmation_page(request):
    """Process the form submission, and generate a result.
    """
    print(request.POST)
    if request.POST:
        template_name = 'restaurant/confirmation.html'
        selected_entrees = request.POST.getlist('entree')
        instructions = request.POST['instructions']
        name = request.POST['customer-name']
        phone = request.POST['customer-phone']
        email = request.POST['customer-email']

        total = 0
        for entree in selected_entrees:
            total += entree_prices[entree]

        special = request.POST.get('special')
        if special:
            total += 3
            selected_entrees.append(special_of_the_day)

        added_minutes = random.randint(30, 60)
        future_time = datetime.now() + timedelta(minutes=added_minutes)

        context = {
            "time": time.ctime(),
            'future_time': future_time,
            'selected_entrees': ', '.join(selected_entrees),
            'instructions': instructions,
            'total': total,
            'name': name,
            'phone': phone,
            'email': email
        }
        return render(request, template_name=template_name, context=context)

    template_name = 'restaurant/order.html'
    return render(request, template_name)
