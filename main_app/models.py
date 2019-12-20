from django.db import models
from django.contrib.auth.models import User


# Create your models here.
sexes = (
    ('M', 'male'),
    ('F', 'female'),
    ('O', 'other'),
)

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  username = models.CharField(max_length=100)
  weight = models.IntegerField()
  sex = models.CharField(max_length=1, choices=sexes)

class Drink(models.Model):
  name = models.CharField(max_length=100)
  drink_type = models.CharField(max_length=100) # choices????
  abv = models.IntegerField()
  cost = models.IntegerField()
  time_consumed = models.DateTimeField()
  effects = models.CharField(max_length=300) # do we need?


class DrinkSession(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  start_time = models.DateTimeField()
  duration = models.TimeField() # should this be integer field?? or maybe even calculated
  drinks = models.ManyToManyField(Drink)
  location = models.CharField(max_length=200) # is this necessary?
  occasion = models.CharField(max_length=200) # should we have choices here?

  # def calc_max_bac(self):
    # Calculation based on drinks and time 


class Photo(models.Model):
  url = models.CharField(max_length=250)
  session = models.ForeignKey(DrinkSession, on_delete=models.CASCADE)
