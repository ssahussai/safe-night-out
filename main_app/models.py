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


