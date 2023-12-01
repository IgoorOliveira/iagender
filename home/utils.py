import re

from .models import Day, Category, Interval, Establishment, EstablishmentDay, Schedules
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
def remove_mask_phone(phone):
    dig = [char for char in phone if char.isdigit()]
    return ''.join(dig)

def mask_phone(phone):
    number = ''.join(c for c in phone if c.isdigit())
    standard = re.compile(r'(\d{2})(\d{5})(\d{4})')
    mask_phone = standard.sub(r'(\1) \2-\3', number)
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


def get_available_hour(service, establishment, intervals, year, month, day):
    available_hours= []
    available_hours_with_service = []
    occupied_times = []
    initial_end_hour = {}
    format = "%H:%M"

    schedules = Schedules.objects.filter(date=date(year, month, day), establishment=establishment).order_by("initial_hour")

    for schedule in schedules:
        initial_end_hour[schedule.initial_hour.strftime(format)] = schedule.end_hour

    for interval in intervals:
        initial_hour = datetime.strptime(interval.initial_interval.strftime(format), format).time()
        end_hour = datetime.strptime(interval.close_interval.strftime(format), format).time()
        current_hour = initial_hour

        while current_hour <= end_hour:
            current_hour_str = current_hour.strftime(format)
            
            if initial_end_hour.get(current_hour_str) is not None:
                while current_hour < datetime.combine(datetime.today(), initial_end_hour[current_hour_str]).time():
                    occupied_times.append(current_hour.strftime(format))
                    current_hour = (datetime.combine(datetime.today(), current_hour) + timedelta(minutes=15)).time()
                
            else:
                available_hours.append(current_hour_str)
                current_hour = (datetime.combine(datetime.today(), current_hour) + timedelta(minutes=15)).time()
    
    for available_hour in available_hours:
        end_time_with_service = (datetime.strptime(available_hour, format) + timedelta(minutes=service.duration.total_seconds() / 60)).strftime(format)
    
        if end_time_with_service not in occupied_times:
            available_hours_with_service.append(available_hour)
        elif (datetime.strptime(end_time_with_service, format) - timedelta(minutes=15)).strftime(format) not in occupied_times:
            available_hours_with_service.append((datetime.strptime(end_time_with_service, format) - timedelta(minutes=service.duration.total_seconds()/60)).strftime(format))
   
    return available_hours_with_service

        


