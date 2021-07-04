from django.db import models

# Create your models here.
class airline(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class city(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class aircraft(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class flights(models.Model):
    airtype = models.ManyToManyField(aircraft, related_name='airtype', blank=True)
    fromlocation = models.ManyToManyField(city, related_name='fromlocation', blank=True)
    tolocation = models.ManyToManyField(city, related_name='tolocation', blank=True)
    airlinename = models.ManyToManyField(airline, related_name='airlinename', blank=True)
