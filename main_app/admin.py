from django.contrib import admin
from .models import Drink, DrinkSession, Photo, Profile

# Register your models here.
admin.site.register(DrinkSession)
admin.site.register(Drink)
admin.site.register(Photo)
admin.site.register(Profile)
