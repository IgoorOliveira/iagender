import re

from .models import Day, Category, Interval, Establishment, EstablishmentDay
from django.contrib.auth.models import User
from datetime import datetime
def remove_mask_phone(phone):
    dig = [char for char in phone if char.isdigit()]
    return ''.join(dig)

def mask_phone(phone):
    number = ''.join(c for c in phone if c.isdigit())
    padrao = re.compile(r'(\d{2})(\d{5})(\d{4})')
    mask_phone = padrao.sub(r'(\1) \2-\3', number)
    return mask_phone

def validate_form(request, formModel):
    fields = formModel().fields.keys()
    form = formModel({field: request[field] for field in fields})
    return form

def create_operating_days(request, establishment_instance, operating_days):
    for day in get_days():
        day = day['name']
        day_instance = Day.objects.get(name=day)
        if day in operating_days:
            establishment_instance.days.add(day_instance, through_defaults={'status': True})
            initial_intervals = request.POST.getlist(f"initial_interval_{day.lower()}")
            close_intervals = request.POST.getlist(f"close_interval_{day.lower()}")

            for index in range(len(initial_intervals)):
                Interval.objects.create(
                    initial_interval=initial_intervals[index],
                    close_interval=close_intervals[index], 
                    day=establishment_instance.establishment_day.order_by('-id').first()
                )
        else:
            establishment_instance.days.add(day_instance, through_defaults={'status': False})

def get_categories():
    categories = Category.objects.all()
    data = list(categories.values())
    return data

def get_days():
    days = Day.objects.all()
    data = list(days.values())
    return data

def get_profile(user):
    return User.objects.get(username=user)

def get_establishment(user):
    establishment = user.establishment
    establishment.phone = mask_phone(establishment.phone)
    return establishment


def get_category(user):
    establishment = user.establishment
    category = establishment.category.first()
    return category

def get_address(user):
    address = user.establishment.adress
    return address

def get_schedule(user):
    schedule = []
    establishment = user.establishment
    days = establishment.establishment_day.all()

    for day in days:
        name = day.day.name
        object_day = {
            "name": name,
            "status": day.status,
            "intervals": []
        }
        intervals = day.intervals.all()
        for interval in intervals:
            object_day["intervals"].append({
                "id": interval.id,
                "initial_interval": interval.initial_interval.strftime("%H:%M"),
                "close_interval": interval.close_interval.strftime("%H:%M")
            })
        schedule.append(object_day)
    return schedule

def get_time(initial_hour, final_hour, interval_min):
    list_time = []
    current_time = initial_hour * 60
    final_min = final_hour * 60

    while current_time <= final_min:
        hours = str(current_time // 60).zfill(2)
        minutes = str(current_time % 60).zfill(2)
        list_time.append(f"{hours}:{minutes}")
        current_time += interval_min

    return list_time






      

