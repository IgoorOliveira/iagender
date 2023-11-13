from django.shortcuts import render
from .models import Category

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'signup.html');

def login(request):
    return render(request, 'signin.html');

def auth_with_email(request):
    categories = get_categories()
    return render(request, 'auth.html', {'categories': categories});


def get_categories():
    categories = Category.objects.all()
    data = list(categories.values())
    return data
