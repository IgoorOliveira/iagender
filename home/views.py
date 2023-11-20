from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import Context
from .models import Account, Category, Adress, Day, Interval, Establishment, EstablishmentDay
from .forms import AccountForm, EstablishmentForm, AdressForm, DayFormSet

from datetime import timedelta

def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'signin.html')

def auth_with_email(request):
    context = {
        "categories": get_categories(),
        "days": get_days()
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

"""def register_intervals(request):
    days_instance = EstablishmentDay.objects.filter(status=True)
    for day_instance in days_instance:
        initial_intervals = request.POST.getlist(f"initial_interval_{day_instance['day'].lower()}")
        close_intervals = request.POST.getlist(f"close_interval_{day_instance['day'].lower()}")
        print(initial_intervals, close_intervals)
        Interval.objects.create(
            initial_interval=initial_intervals[index],
            close_interval=close_intervals[index], 
            day=day_instance
        )
    """

def create_operating_days(request, establishment_instance, operating_days):
    for day in get_days():
        operating_day_instance = Day.objects.get(day=day['day'])

        if day['day'] in operating_days:
            establishment_instance.days.add(operating_day_instance, through_defaults={'status': True})
            initial_intervals = request.POST.getlist(f"initial_interval_{day['day'].lower()}")
            close_intervals = request.POST.getlist(f"close_interval_{day['day'].lower()}")

            for index in range(len(initial_intervals)):
                Interval.objects.create(
                    initial_interval=initial_intervals[index],
                    close_interval=close_intervals[index], 
                    day=establishment_instance.establishment_day.order_by('-id').first()
                )
        else:
            establishment_instance.days.add(operating_day_instance, through_defaults={'status': False})

      

def get_user(request):
    return render(request, "dashboard.html")
    if request.method == 'POST':

        form_account = validate_form(request.POST, AccountForm)
        form_adress = validate_form(request.POST, AdressForm)
        form_company = validate_form(request.POST, EstablishmentForm)
        category_name = request.POST.get('category_name')
        operating_days = request.POST.getlist("day")
        

        if all([form.is_valid() for form in [form_adress, form_account, form_company]]) and Category.objects.filter(category_name=category_name).exists():
            account = form_account.save()
            adress = form_adress.save()
    
            establishment_instance = form_company.save(commit=False)
            establishment_instance.account = account
            establishment_instance.adress = adress
            establishment_instance.save()
            create_operating_days(request, establishment_instance, operating_days)


    
            establishment_instance.category.add(Category.objects.get(category_name=category_name))

        else:
            return redirect('auth')


def validate_form(request, formModel):
    fields = formModel().fields.keys()
    form = formModel({field: request[field] for field in fields})
    return form