from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import datetime
import math

# Create your models here.
sexes = (
    ('M', 'male'),
    ('F', 'female'),
    ('O', 'other'),
)

drinks = (
    ('B', 'beer'),
    ('W', 'wine'),
    ('L', 'liquor'),
    ('C', 'cocktail'),
    ('S', 'spiked'),
)

bac_inteval = 15 # in minutes

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  username = models.CharField(max_length=100)
  weight = models.IntegerField()
  sex = models.CharField(max_length=1, choices=sexes)

  def __str__(self):
    return f"{self.username}'s profile"

class Drink(models.Model):
  name = models.CharField(max_length=100)
  drink_type = models.CharField(max_length=100, choices=drinks)
  abv = models.IntegerField()  # default??? beer 5%, wine 12%, liquor 40%?
  cost = models.IntegerField()

  def get_absolute_url(self):
    return reverse('drinks_detail', kwargs={'pk': self.id})

  def __str__(self):
    return f"{self.name}"

class DrinkSession(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  start_time = models.DateField()
  duration = models.IntegerField() # should this be integer field?? or maybe even calculated

  def calc_bac(self):
    bac_dict = {}
    
    # get drink events, NOTE: sorted in order at drinktime model
    drink_events = self.drinktime_set.all()
    if drink_events:
      first_dt = drink_events[0].time_consumed
      starting_minute = math.floor(first_dt.minute % bac_inteval)*bac_inteval
      start = drink_events[0].time_consumed.replace(second=0, minute=starting_minute)
      print(start)
      print(start.strftime('%X'))
      bac_dict[start.strftime('%X')] = 0

    # loop through drink events and add data to bac_dict
      for d in drink_events:

        print(d.time_consumed)



    return bac_inteval
    # Calculation based on drinks and time 

  def __str__(self):
    return f"drinking on {self.start_time}"
  
  def get_absolute_url(self):
    return reverse('detail', kwargs={'session_id': self.id})

class DrinkTime(models.Model):
  time_consumed = models.TimeField()
  effects = models.CharField(max_length=300)
  drink = models.ForeignKey(Drink,on_delete=models.CASCADE)
  session = models.ForeignKey(DrinkSession,on_delete=models.CASCADE)

  class Meta:
    ordering = ['time_consumed']

class Photo(models.Model):
  url = models.CharField(max_length=250)
  session = models.ForeignKey(DrinkSession, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for session_id: {self.session_id} @{self.url}"

