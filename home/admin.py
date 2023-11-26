from django.contrib import admin
from .models import Category, EstablishmentDay ,Day, Establishment, Adress, Interval, Service
# Register your models here.

admin.site.register(Category)
admin.site.register(EstablishmentDay)
admin.site.register(Establishment)
admin.site.register(Adress)
admin.site.register(Interval)
admin.site.register(Service)
admin.site.register(Day)
