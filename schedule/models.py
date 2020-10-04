from django.db import models
from PSQI.models import PSQI
from django.utils import timezone
from datetime import date, timedelta
import datetime
from django.urls import reverse
from sleep.models import Sleep
from .calculations import recommendation, Action

import math
import os

from django.db.models.signals import post_save

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sleep_schedule.settings')


# Create your models here.
class Sleep_schedule(models.Model):

    date = models.DateField()

    start_time = models.TimeField(default=datetime.time(23, 00))
    end_time = models.TimeField(default=datetime.time(8, 00))

    take_meditation = models.BooleanField(default=False,blank=True, null=True)
    take_melatonin = models.BooleanField(default=False,blank=True, null=True)
    take_caffeine = models.BooleanField(default=False,blank=True, null=True)
    take_nap = models.BooleanField(default=False,blank=True, null=True)

    nap_start = models.TimeField(blank=True, null=True, default=datetime.time(14, 00))
    nap_end = models.TimeField(blank=True, null=True, default=datetime.time(15, 00))

    resistant_excercise_start = models.TimeField(blank=True, null=True, default=datetime.time(15, 00))
    resistant_excercise_end = models.TimeField(blank=True, null=True, default=datetime.time(15, 30))
    aerobics_exercise_start = models.TimeField(blank=True, null=True, default=datetime.time(15, 30))
    aerobics_exercise_end = models.TimeField(blank=True, null=True, default=datetime.time(16, 00))


    breakfast_start_time = models.TimeField(default=datetime.time(8, 00))
    breakfast_end_time = models.TimeField(default=datetime.time(8, 15))
    lunch_start_time = models.TimeField(default=datetime.time(12, 00))
    lunch_end_time = models.TimeField(default=datetime.time(12, 30))
    dinner_start_time = models.TimeField(default=datetime.time(18, 00))
    dinner_end_time = models.TimeField(default=datetime.time(19, 00))

    sensed_score = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    PSQI_score = models.IntegerField(max_length=200, blank=True, null=True)



    def __str__(self):
        return '%s "sleep schedule"' % (self.date)

    def get_absolute_url(self):
        # return f'/product/{self.id}'
        return reverse("schedule:schedule_detail", kwargs={"id": self.id})

    def update_sensed_score(self, score):
        self.sensed_score = score
        self.save()


    def update_PSQI_score(self, score):
        self.PSQI_score = score
        self.save()


    def sleep_more(self):
    
        delta = datetime.timedelta(hours = 0.5)
        new_start_time = (datetime.datetime.combine(datetime.date(1,1,1),self.start_time) - delta).time()
        self.start_time = new_start_time
        self.save()

    def sleep_less(self):
        delta = datetime.timedelta(hours = 0.5)
        new_start_time = (datetime.datetime.combine(datetime.date(1,1,1),self.start_time) + delta).time()
        self.start_time = new_start_time
        self.save()

    def add_meditation(self):
        self.take_meditation = True
        self.save()

    def add_nap(self):
        self.take_nap = True
        self.save()

    def add_melatonin(self):
        self.take_melatonin = True
        self.save()

    def add_coffeine(self):
        self.take_caffeine = True
        self.save()



    

date = date.today() + timedelta(days=7)
start_time = timezone.now()
end_time = timezone.now()
nap_start = timezone.now()
nap_end = timezone.now()


# Once submit PSQI, automatically create +7 day schedule with default value
def create_schedule(sender, **kwargs):
    if kwargs['created']:

        sleep_schedule = Sleep_schedule.objects.create(
            date = date,
            start_time = start_time,
            end_time = end_time,
            nap_start = nap_start,
            nap_end = nap_end,
            
        )


# Once submit PSQI, automatically update today's schedule based on PSQI and sensor data
def update_schedule(sender, instance, **kwargs):
    if kwargs['created']:

        # Previous date to get sleep data
        previous_date = date.today() - timedelta(days=1)
        # Get sleep object
        sleep = Sleep.objects.get(date=previous_date)
        # Get today schedule object
        today_schedule = Sleep_schedule.objects.filter(date=date.today())[0]

        # Get scores
        sleep_sensed_score = sleep.get_sleep_score()
        PSQI_score = instance.get_score(sleep.latency, sleep.duration, sleep.efficiency)

        # Update scores to schedule
        today_schedule.update_sensed_score(sleep_sensed_score)
        today_schedule.update_PSQI_score(PSQI_score)

        # Get recommendations
        rec = recommendation(PSQI_score, sleep_sensed_score, sleep.duration, sleep.latency)

        for i in rec:
            # Remain wake up time
            if i == Action.SLEEP_MORE:
                add_to_sleep_start = -datetime.timedelta(hours = 1)
                today_schedule.sleep_more()

            elif i == Action.SLEEP_LESS:
                add_to_sleep_start = datetime.timedelta(hours = 1)
                today_schedule.sleep_less()

            elif i == Action.MEDITATION:
                today_schedule.add_meditation()
            
            elif i == Action.TAKE_NAP:
                today_schedule.add_nap()
            
            elif i == Action.Melatonin:
                today_schedule.add_melatonin() 

        


#post_save.connect(create_schedule, sender = PSQI)
post_save.connect(update_schedule, sender = PSQI)


