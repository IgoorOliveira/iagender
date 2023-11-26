from django.db import models
from django.contrib.auth.models import User



class Adress(models.Model):
    street = models.CharField(max_length=255)
    cep = models.CharField(max_length=14)
    neighborhood = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    uf = models.CharField(max_length=30)
    number = models.CharField(max_length=20)
    complement = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.street

class Category(models.Model):
    category_name = models.CharField(name="category_name", max_length=50, unique=True)
    id_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class Day(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


    
class Establishment(models.Model):
    company_name = models.CharField(name="company_name", max_length=100, blank=True)
    phone = models.CharField(max_length=14)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="establishment")
    adress = models.OneToOneField(Adress, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    days = models.ManyToManyField(Day, through="EstablishmentDay", related_name="establishment")
    

    def __str__(self):
        return self.company_name
    
class EstablishmentDay(models.Model):
    name = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name="establishment_day")
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="establishment_day")
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name.company_name} - {self.day.name} - {'Aberto' if self.status else 'Fechado'}"
    
    
class Interval(models.Model):
    initial_interval = models.TimeField(max_length=5)
    close_interval = models.TimeField(max_length=5)
    day = models.ForeignKey(EstablishmentDay, on_delete=models.CASCADE, related_name="intervals")

    def __str__(self):
        return f"{self.initial_interval} - {self.close_interval}" 
    
class Service(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE, related_name="services")

    def __str__(self):
        return f"{self.name} - {self.establishment}"