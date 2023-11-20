from django import forms
from django.forms import modelform_factory

from .models import Account, Establishment, Category, Adress, Interval, EstablishmentDay

"""class MultiStepForm:
    name = forms.CharField(min_length=4, max_length=100, validators=[])
    email = forms.EmailField(max_length=320)
    password = forms.CharField()


    companyName = forms.CharField(max_length=100, required=False)
    userUrl = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=11)


    category = forms.CharField(max_length=30)
    

    cep = forms.CharField(max_length=8)
    logradouro = forms.CharField(max_length=255)
    city = forms.CharField(max_length=50)
    uf = forms.CharField(max_length=2)
    neighboard = forms.CharField(max_length=50)
    number = forms.CharField(max_length=10)
    complement = forms.CharField(max_length=100, required=False)

"""


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"


class AdressForm(forms.ModelForm):
    class Meta:
        model = Adress
        fields = "__all__"

class EstablishmentForm(forms.ModelForm):
    class Meta:
        model = Establishment
        exclude = ['account', 'adress', 'category', 'days']

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

DayFormSet = modelform_factory(EstablishmentDay, exclude=['status'])
