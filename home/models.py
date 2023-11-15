from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    id_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


"""class Account(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=320, unique=True)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=14)

    def __str__(self):
        return self.nome
    
class establishment(models.Model):
    name = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=20)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category,)

    def __str__(self):
        return self.nome

class Adress(models.Model):
    street = models.CharField(max_length=255)
    cep = models.CharField(max_length=14)
    bairro = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    estado = models.CharField(max_length=30)
    number = models.CharField(max_length=20)
    complement = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nome

class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    duration = models.DurationField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome




class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.nome"""



class Day(models.Model):
    name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

class Interval(models.Model):
    initialInterval = models.TimeField(max_length=5)
    closeInterval = models.TimeField(max_length=5)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.initialInterval} x {self.closeInterval}" 



    def __str__(self):
        return self.name
 

