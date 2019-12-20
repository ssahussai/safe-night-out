from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


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
  drink_type = models.CharField(max_length=100, choices=drinks) # choices????
  abv = models.IntegerField()  # default??? beer 5%, wine 12%, liquor 40%?
  cost = models.IntegerField()
  time_consumed = models.DateTimeField()
  effects = models.CharField(max_length=300) 

  # def __save___(self):

  def __str__(self):
    return f"{self.name}"

class DrinkSession(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  start_time = models.DateTimeField()
  duration = models.IntegerField() # should this be integer field?? or maybe even calculated
  drinks = models.ManyToManyField(Drink)

  # def calc_bac(self):
    # Calculation based on drinks and time 

  def __str__(self):
    return f"drinking on {self.start_time} at {self.location}"
  
  def get_absolute_url(self):
    return reverse('detail', kwargs={'session_id': self.id})


class Photo(models.Model):
  url = models.CharField(max_length=250)
  session = models.ForeignKey(DrinkSession, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for session_id: {self.session_id} @{self.url}"

