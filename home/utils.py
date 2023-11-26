from .models import Day, Category, Interval
def remove_mask_phone(phone):
    dig = [char for char in phone if char.isdigit()]
    return ''.join(dig)

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


      

