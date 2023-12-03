from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from .utils import remove_mask_phone, create_operating_days, validate_form, get_categories, get_days, get_profile, get_establishment, get_address, get_category, get_schedule, get_time, get_available_hour, format_duration
from django.http import HttpResponse, JsonResponse
from .models import Category, Adress, Day, Interval, Establishment, EstablishmentDay, Schedules, Client, Service
from .forms import EstablishmentForm, AdressForm, ServiceForm, CategoryForm, ClientForm
from urllib.parse import urlencode
from datetime import date, timedelta, datetime

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
        user = User.objects.get(email=email)
        

        if user is not None:
            user = authenticate(username=user.username, password=password)
        else:
            return redirect("login")
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return redirect("login")


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
def schedule(request, date_url):
    if request.method == "GET":

        establishment = request.user.establishment

        schedules = Schedules.objects.filter(establishment=establishment, date=date_url)

        context = {
            "schedule": schedule
        }

        return render(request, "schedule.html", context=context)      


def get_available_times(request, username, service, date_url):

    if request.method == "GET":
        context = {
            "operating_days": {}
        }
        day_en_ptbr = {
            "Monday": "Segunda",
            "Tuesday": "Terça",
            "Wednesday": "Quarta",
            "Thursday": "Quinta",
            "Friday": "Sexta",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }
        year, month = [int(i) for i in date_url.split("-")]


        user = User.objects.get(username=username)
        establishment = user.establishment
        service_instance = Service.objects.get(slug=service)

        days = EstablishmentDay.objects.filter(name=establishment, status=True)
        available_day_week = [day.day.name for day in days]

        first_day_next_month = date(year, month, 1) + timedelta(days=32)
        last_day_month = (first_day_next_month.replace(day=1) - timedelta(days=1)).day

        for day in range(1, last_day_month + 1):
            
            day_week = date(year, month, day).strftime("%A")

            if day_en_ptbr[day_week] in available_day_week:
                day_instance = Day.objects.get(name=day_en_ptbr[day_week])
                establishment_day = EstablishmentDay.objects.get(name=establishment, day=day_instance)
                intervals = establishment_day.intervals.all()

                context["operating_days"][day] = get_available_hour(service_instance, establishment, intervals, year, month, day)
        return JsonResponse(context)

@login_required
def get_operating_days(request, date_url):

    if request.method == "GET":
        operating_days = []
        weekdays = {
            1: "Segunda",
            2: "Terça",
            3: "Quarta",
            4: "Quinta",
            5: "Sexta",
            6: "Sábado",
            7: "Domingo",
        }

        days = request.user.establishment.establishment_day.filter(status=True)
        available_day_week = [day.day.name for day in days]
        year, month, day = [int(i) for i in date_url.split("-")]
        first_day_next_month = date(year, month, 1) + timedelta(days=32)
        last_day_month = (first_day_next_month.replace(day=1) - timedelta(days=1)).day

        for day in range(1, last_day_month + 1):
            day_of_week = date(year, month, day).weekday()

            if weekdays[day_of_week + 1] in available_day_week:
                operating_days.append(day)

        return JsonResponse(operating_days, safe=False)

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
    else:
        form = ServiceForm(request.POST)

        if form.is_valid():
            form.save()
    
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


def get_page(request, username):
    user = User.objects.get(username=username)
    
    if user:
        context = {
            "user": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
            },
            "address": user.establishment.adress,
            "services": user.establishment.services.all(),
            "date": datetime.now().strftime('%Y-%m')
        }
    

    if request.method == "GET":
        return render(request, "page-profissional.html", context=context)
    

def get_details_date(request, username, service, date):
    
    if request.method == "GET":
        return render(request, "page-date.html")
    
def get_client(request, username, service, date_url, time):
    year, month, day = [int(i) for i in date_url.split("-")]
    date_instance = date(year, month, day)

    day_en_ptbr = {
        "Monday": "Segunda-feira",
        "Tuesday": "Terça-feira",
        "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira",
        "Friday": "Sexta-feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }

    name_month = {
        1: "janeiro",
        2: "fevereiro",
        3: "março",
        4: "abril",
        5: "maio",
        6: "junho",
        7: "julho",
        8: "agosto",
        9: "setembro",
        10: "outubro",
        11: "novembro",
        12: "dezembro"
    }
    if request.method == "GET":


        service_instance = Service.objects.get(slug=service)
        service_name = service_instance.name
        service_duration = format_duration(service_instance.duration)


        date_schedule = f"{day_en_ptbr[date_instance.strftime('%A')]}, {day} de {name_month[month]} de {year}"

        context = {
            "username": username,
            "service": service,
            "date_url": date_url,
            "time": time,
            "service_name": service_name,
            "service_duration": service_duration,
            "date_schedule": date_schedule
        }

        return render(request, "page-client.html", context=context)
    else:
        user = User.objects.get(username=username)
        service_instance = Service.objects.get(slug=service)
        if user:

            form_client = validate_form(request.POST, ClientForm)
            

            if form_client.is_valid():
                client_instance = None
                client = Client.objects.filter(email=request.POST.get("email")).first()
                if client is not None:
                    client_instance = client
                else:
                    client_instance = form_client.save()

                hours, remainder = divmod(service_instance.duration.total_seconds(), 3600)
                minutes, _ = divmod(remainder, 60)

                initial_hour_datetime = datetime.strptime(time, "%H:%M")
                end_hour_datetime = initial_hour_datetime + timedelta(hours=int(hours)) + timedelta(minutes=int(minutes))

                schedule = Schedules.objects.create(
                    date = date_instance,
                    initial_hour = initial_hour_datetime,
                    end_hour = end_hour_datetime,
                    client = client,
                    service = service_instance,
                    establishment = user.establishment
                )
                schedule.save()

                url = reverse("get_page", args=[username])
            else:
                return HttpResponse(form_client.errors)
        else:
            return HttpResponse("user não encontrado")
        
        url = reverse("get_page", args=[username])
        return redirect(url)

    

    



        








