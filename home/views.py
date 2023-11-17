from django.shortcuts import render 
from django.http import HttpResponse
from django.template import Context
from .models import Category, Day

from datetime import timedelta

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'signup.html');

def login(request):
    return render(request, 'signin.html')

def auth_with_email(request):
    context = {
        "categories": get_categories(),
        "days": get_days(),
    }
    
    return render(request, 'auth.html',context=context)


def get_categories():
    categories = Category.objects.all()
    data = list(categories.values())
    return data


def get_days():
    days = Day.objects.all()
    data = list(days.values())
    return data

