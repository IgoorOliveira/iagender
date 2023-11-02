from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'signup.html');

def login(request):
    return render(request, 'signin.html');

def auth_with_email(request):
    return render(request, 'auth.html');
