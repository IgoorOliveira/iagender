from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from .utils import remove_mask_phone, create_operating_days, validate_form, get_categories, get_days, get_profile, get_establishment, get_address, get_category, get_schedule, get_time
from django.http import HttpResponse, JsonResponse
from .models import Category, Adress, Day, Interval, Establishment, EstablishmentDay
from .forms import EstablishmentForm, AdressForm, ServiceForm, CategoryForm

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

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            return redirect("/login")


def get_user(request):
    context = {
        "categories": get_categories(),
        "days": get_days(),
        "times": get_time(0, 23, 15)
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
                return redirect('dashboard/')

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
    context = {
        "categories": get_categories(),
        "days": get_days()
    }
    if request.method == "GET":
        return render(request, "settings.html", context)
    
@login_required
def update_profile(request):
    context = {
        "user": get_profile(request.user)
    }
    if request.method == 'GET':
        return render(request, "settings-profile.html", context)
    else:
        user = request.user
        name = request.POST.get("name").split()
        email = request.POST.get("email")

        first_name = name[0]
        last_name = name[-1]

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        return redirect("/settings/profile")
    
@login_required
def update_company(request):
    context = {
        "user": get_profile(request.user),
        "company": get_establishment(request.user)
    }
    if request.method == 'GET':
        return render(request, "settings-company.html", context)
    else:
        user = request.user
        form = EstablishmentForm(request.POST.copy(), instance=user.establishment)

        if "phone" in form.data:
            form.data['phone'] = remove_mask_phone(form.data['phone'])

        if form.is_valid():
            user.username = request.POST.get("username")
            user.save()
            form.save()
        return redirect("/settings/company")
    
@login_required
def update_category(request):
    category = get_category(request.user).category_name
    context = {
        "categories": get_categories(),
        "active_category": category
    }
    if request.method == 'GET':
        return render(request, "settings-category.html", context)
    else:
        establishment = request.user.establishment
        category = Category.objects.get(establishment=establishment)
        establishment.category.set(request.POST.get("category_name"))
        

        return redirect("/settings/category")
    
@login_required
def update_address(request):
    context = {
        "address": get_address(request.user)
    }
    if request.method == 'GET':
        return render(request, "settings-address.html", context)
    else:
        establishment = request.user.establishment
        form = AdressForm(request.POST, instance=establishment.adress)

        if form.is_valid():
            form.save()

        return redirect("/settings/address")
        
    
@login_required
def get_settings_schedule(request):
    context = {
        "days": get_schedule(request.user),
        "times": get_time(0, 23, 15)
    }
    if request.method == 'GET':
        return render(request, "settings-schedule.html", context)


@login_required
def update_schedule(request):
    context_days = get_schedule(request.user)

    if request.method == "POST":
        operating_days = request.POST.getlist("day")
        day_add = []
        day_remove = []
    
        for day in context_days:
            if day["name"] not in operating_days and day["status"]:
                day_remove.append(day["name"])
            if day["name"] in operating_days and not(day["status"]):
                day_add.append(day["name"])
            

        establishment = request.user.establishment
        days = establishment.establishment_day.all()

        for day in days:
            name = day.day.name
            if name in day_add:
                day.status = True
            elif name in day_remove:
                day.status = False
            
            initial_intervals = request.POST.getlist(f"initial_interval_{name.lower()}")
            close_intervals = request.POST.getlist(f"close_interval_{name.lower()}")

            intervals = day.intervals.all()
            for index in range(len(initial_intervals)):
                initial_interval, close_interval = initial_intervals[index], close_intervals[index]
                interval_exist = intervals.filter(initial_interval = initial_interval, close_interval = close_interval).exists()

                if not(interval_exist):
                    Interval.objects.create(
                        initial_interval = initial_interval,
                        close_interval = close_interval,
                        day = day
                    )
            
            day.save()

        return redirect("/settings/schedule")

def delete_interval(request, id):
    if request.method == "GET":
        Interval.objects.get(id=id).delete()
    return redirect("/settings/schedule")


def get_page(request):
    if request.method == "GET":
        return render("page-profissional.html")

        









