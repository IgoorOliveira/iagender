from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from .utils import remove_mask_phone, create_operating_days, validate_form, get_categories, get_days
from django.http import HttpResponse, JsonResponse
from .models import Category, Adress, Day, Interval, Establishment, EstablishmentDay
from .forms import EstablishmentForm, AdressForm, ServiceForm

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'signup.html')

def login_user(request):
    if request.method == "GET":
        return render(request, 'signin.html')
    else:
        email = request.POST["email"]
        password = request.POST["password"]
        username = User.objects.get(email=email).username

        a = authenticate(username=username, password=password)
        print(email, password)
        print(a)
        if a is not None:
            login(request, a)
            return redirect("/dashboard")
        else:
            return redirect("/login")


def get_user(request):
    context = {
        "categories": get_categories(),
        "days": get_days()
    }

    if request.method == 'POST':
        form_address = validate_form(request.POST, AdressForm)
        form_company = validate_form(request.POST.copy(), EstablishmentForm)

        category_name = request.POST.get('category_name')
        operating_days = request.POST.getlist("day")

        if "phone" in form_company.data:
            form_company.data['phone'] = remove_mask_phone(form_company.data['phone'])

        username = request.POST.get("username")
        name = request.POST.get("name").split()
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not User.objects.filter(email=email).exists():
            if all([form.is_valid() for form in [form_address, form_company]]) and Category.objects.filter(
                    category_name=category_name).exists():

                user = User.objects.create(
                    username=username,
                    email=email,
                    password=password,
                    first_name=name[0],
                    last_name=name[-1],
                )
                user.set_password(password)
                user.save()
                address = form_address.save()

                establishment_instance = form_company.save(commit=False)
                establishment_instance.user = user
                establishment_instance.adress = address
                establishment_instance.save()
                create_operating_days(request, establishment_instance, operating_days)

                establishment_instance.category.add(Category.objects.get(category_name=category_name))
                return redirect('dashboard')

        return redirect("/")
    else:
        return render(request, "auth.html", context=context)
    
@login_required
def logout_user(request):
    if request.method == "GET":
        logout(request)
        return redirect("/")


@login_required
def dashboard(request):
    if request.method == "GET":
        return render(request, "dashboard.html")
        

@login_required
def get_operating_days(request):
    context = {}
    list_operating_days = []
    if request.method == "GET":
        establishment_instance = request.user.establishment
        establishment_days = EstablishmentDay.objects.filter(name_id=establishment_instance, status=True).select_related("name")
        for establishment_day in establishment_days:
            day_name = establishment_day.day.name
            list_operating_days.append(day_name)
        context["operating_days"] = list_operating_days
    return JsonResponse(context)

@login_required
def get_services(request):
    if request.method == "GET":
        return render(request, 'services.html')
    else:
        form = ServiceForm(request.POST.copy())
        if 'duration' in form.data:

            form.data['duration'] = form.data['duration'][:-1]

        if form.is_valid():
            service_instance = form.save(commit=False)
        return redirect("services")

@login_required
def get_settings(request):
    if request.method == "GET":
        return render(request, "settings.html")


