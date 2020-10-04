from django.db import models
from PSQI.models import PSQI
from django.utils import timezone
from datetime import date, timedelta
import datetime
from django.urls import reverse
from sleep.models import Sleep
from .calculations import recommendation, Action
from astronauts.models import Astronaut 
from exercises.models import Exercise


import math
import os

from django.db.models.signals import post_save

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sleep_schedule.settings')


# Create your models here.
class Sleep_schedule(models.Model):

    astronaut = models.ForeignKey(Astronaut, on_delete=models.CASCADE, null=True, blank=True, default = 1)
    exercise = models.OneToOneField(Exercise, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    day = models.IntegerField(default = 1, null= True, blank=True)

    

    start_time = models.TimeField(blank=True, null=True, default=datetime.time(23, 00))
    end_time = models.TimeField(blank=True, null=True, default=datetime.time(8, 00))

    take_meditation = models.BooleanField(default=False,blank=True, null=True)
    take_melatonin = models.BooleanField(default=False,blank=True, null=True)
    take_caffeine = models.BooleanField(default=False,blank=True, null=True)
    take_nap = models.BooleanField(default=False,blank=True, null=True)

    nap_start = models.TimeField(blank=True, null=True, default=datetime.time(14, 00))
    nap_end = models.TimeField(blank=True, null=True, default=datetime.time(15, 00))

    do_resistant = models.BooleanField(default=True,blank=True, null=True)
    do_aerobics = models.BooleanField(default=True,blank=True, null=True)
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
    PSQI_score = models.IntegerField(blank=True, null=True)

    light_work_hrs = models.DecimalField(max_digits=3, decimal_places=2, default=4)
    heavy_work_hrs = models.DecimalField(max_digits=3, decimal_places=2, default=4)



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

    def get_exercise_hour(self):

        aerobics_duration = get_time_in_hr(self.aerobics_exercise_start, self.aerobics_exercise_end)
        resistant_duration = get_time_in_hr(self.resistant_excercise_start, self.resistant_excercise_end)
        
        return aerobics_duration + resistant_duration

    def get_meal_hour(self):

        b_duration = get_time_in_hr(self.breakfast_start_time, self.breakfast_end_time)
        l_duration = get_time_in_hr(self.lunch_start_time, self.lunch_end_time)
        d_duration = get_time_in_hr(self.dinner_start_time, self.dinner_end_time)

        return b_duration + l_duration + d_duration
    

    def get_sleep_duration(self):
        
        sleep_duration = get_time_in_hr(self.start_time, self.end_time)
        nap_duration = 0
        if self.take_nap:
            nap_duration = get_time_in_hr(self.nap_start, self.nap_end)
        

        return nap_duration+sleep_duration

    def update_excercise_in_schedule(self, do_exercise, aredTime, aerobicTime, load, instance):
        
        print('!!!!!!!!!!')
        print(aredTime)
        print(aerobicTime)
        print('!!!!!!!!!!')


        self.exercise = instance
        if do_exercise == False: 
            self.do_resistant = False
            self.do_aerobics = False
        else:
            if aredTime == 0:
                self.do_resistant = False
                
            if aerobicTime == 0:
                self.do_aerobics = False

            if aredTime != None:
                delta = datetime.timedelta(hours = aredTime)
                new_reisitant_end_time = (datetime.datetime.combine(datetime.date(1,1,1),self.resistant_excercise_end) + delta).time()            
                self.resistant_excercise_end = new_reisitant_end_time

            if aerobicTime != None:

                self.aerobics_exercise_start = new_reisitant_end_time
                delta2 = datetime.timedelta(hours = aerobicTime)
                new_aerobic_end_time = (datetime.datetime.combine(datetime.date(1,1,1),new_reisitant_end_time) + delta2).time()            
                self.aerobics_exercise_end = new_aerobic_end_time
        
        self.save()
            
        


def get_time_in_hr(start, end):

    start = str(start)
    end = str(end)
    time1 = datetime.datetime.strptime(start,'%H:%M:%S')
    time2 = datetime.datetime.strptime(end,'%H:%M:%S')
    difference = time2-time1
    datetime.timedelta(0, 3600)
    second = difference.seconds
    hours = second/3600
    return hours


tomorrow_date = date.today() + timedelta(days=1)



# Once submit PSQI, automatically create +7 day schedule with default value
def create_schedule(sender, **kwargs):
    if kwargs['created']:

        sleep_schedule = Sleep_schedule.objects.create(
            date = tomorrow_date,
    
        )


# Once submit PSQI, automatically update today's schedule based on PSQI and sensor data
# Changed - Once PSQI created --> Excercise update --> schedue update!!!
def update_schedule(sender, instance, **kwargs):
    if not kwargs['created']:
        PSQI = instance.PSQI

        # Previous date to get sleep data
        previous_date = instance.date - timedelta(days=1)
        # Get sleep object
        sleep = Sleep.objects.get(date=previous_date)
        # Get today schedule object
        today_schedule = Sleep_schedule.objects.filter(date=instance.date)[0]

        # Get scores
        sleep_sensed_score = sleep.get_sleep_score()
        PSQI_score = PSQI.get_score(sleep.latency, sleep.duration, sleep.efficiency)

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
            
            elif i == Action.TAKE_MELATONIN:
                today_schedule.add_melatonin()

        today_schedule.update_excercise_in_schedule(instance.do_exercise, instance.aredTime, instance.aerobicTime, instance.load, instance)



# post_save.connect(create_schedule, sender = PSQI)
post_save.connect(update_schedule, sender = Exercise)


