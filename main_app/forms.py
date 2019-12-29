from django.forms import ModelForm
from .models import DrinkTime, Drink

class DrinkTimeForm(ModelForm):
  class Meta:
    model = DrinkTime
    fields = ['drink', 'effects','time_consumed']