from django import forms
from django.forms import modelform_factory

from .models import Establishment, Category, Adress, Interval, EstablishmentDay, Service



class AdressForm(forms.ModelForm):
    class Meta:
        model = Adress
        fields = "__all__"

class EstablishmentForm(forms.ModelForm):
    class Meta:
        model = Establishment
        exclude = ['user', 'adress', 'category', 'days']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ['id_name']

class IntervalForm(forms.ModelForm):
    class Meta:
        model = Interval
        fields = "__all__"

class OperatingDayForm(forms.ModelForm):
    class Meta:
        model = EstablishmentDay
        fields = "__all__"

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "duration", "description"]



DayFormSet = modelform_factory(EstablishmentDay, exclude=['status'])
