from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import timedelta, datetime, date, time
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

ethanol_density = 789  # g/l
liver_detox_rate = .015 # g/dl/hr
bac_inteval = 15  # in minutes


def get_vol(drink_type):
    if drink_type == 'B':
        return 12
    if drink_type == 'W':
        return 5
    if drink_type == 'L':
        return 1.5
    if drink_type == 'C':
        return 5
    if drink_type == 'S':
        return 12


def calc_bac(curr_bac, min_passed, sex, weight, d=False):
    absorb_frac = .68 if sex == 'M' else .55
    absorb_weight = absorb_frac * weight * 454
    if d:
        vol = get_vol(d.drink_type)
        g_consumed = ethanol_density * vol * 29.57 * d.abv / 1000
        new_bac = g_consumed / absorb_weight * 100
        return new_bac + curr_bac
    return curr_bac  - liver_detox_rate * 100 / (60/min_passed)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    weight = models.IntegerField()
    sex = models.CharField(max_length=1, choices=sexes)

    def __str__(self):
        return f"{self.username}'s profile"

    def get_absolute_url(self):
        return reverse('index')


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
    # should this be integer field?? or maybe even calculated
    duration = models.IntegerField()

    def bac_info(self):
        bac_list = []  # can also make this dictionary
        # get drink events, NOTE: sorted in order at drinktime model
        drink_events = self.drinktime_set.all()
        if drink_events:
            # initialize bac list
            first_dt = drink_events[0].time_consumed
            # get first starting point divisible by time interval
            starting_minute = math.floor(
                first_dt.minute / bac_inteval)*bac_inteval
            start = drink_events[0].time_consumed.replace(
                second=0, minute=starting_minute)
            first_bac = [start, 0]
            bac_list.append(first_bac)
            # get user info
            w = self.user.profile.weight
            s = self.user.profile.sex

        # loop through drink events and add data to bac_dict
            for i in range(len(drink_events)):
                # append new drink
                new_time = datetime.combine(date.min, bac_list[-1][0]) + timedelta(minutes=bac_inteval)
                bac = calc_bac(bac_list[-1][1], bac_inteval, s, w, drink_events[i].drink)
                bac_list.append([new_time.time(),bac])

                # if not user's last drink
                if ((i+1) < len(drink_events)):
                    # countdown, reducing body's bac until user drinks again
                    while ((datetime.combine(date.min, drink_events[i+1].time_consumed)
                     - datetime.combine(date.min, bac_list[-1][0]))
                        > timedelta(minutes=bac_inteval)):
                        new_time = datetime.combine(date.min, bac_list[-1][0]) + timedelta(minutes=bac_inteval)
                        bac = calc_bac(bac_list[-1][1], bac_inteval, s, w)
                        bac = 0 if (bac<0) else bac 
                        bac_list.append([new_time.time(),bac])
            #after last drink, reducing body's bac until it reaches 0 
            while (bac_list[-1][1] > 0):
                new_time = datetime.combine(date.min, bac_list[-1][0]) + timedelta(minutes=bac_inteval)
                bac = calc_bac(bac_list[-1][1], bac_inteval, s, w)
                bac = 0 if (bac<0) else bac 
                bac_list.append([new_time.time(),bac])
        return bac_list

    def __str__(self):
        return f"drinking on {self.start_time}"

    def get_absolute_url(self):
        return reverse('detail', kwargs={'session_id': self.id})


class DrinkTime(models.Model):
    time_consumed = models.TimeField()
    effects = models.CharField(max_length=300)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    session = models.ForeignKey(DrinkSession, on_delete=models.CASCADE)

    class Meta:
        ordering = ['time_consumed']


class Photo(models.Model):
    url = models.CharField(max_length=250)
    session = models.ForeignKey(DrinkSession, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for session_id: {self.session_id} @{self.url}"
