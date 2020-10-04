# Create your models here.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import datetime

# from prizes.models import Prize
import math


# Create your models here.
class Sleep(models.Model):
    date = models.DateField()

    duration = models.IntegerField(default=240)
    efficiency = models.DecimalField(max_digits=3, decimal_places=2, default=0.8)
    start_time = models.TimeField(default=datetime.time(23, 00))
    end_time = models.TimeField(default=datetime.time(8, 00))
    latency = models.IntegerField(default=10)
    body_temperature = models.IntegerField(default=36)
    # Restfulness = wake/total sleep
    restfulness = models.DecimalField(max_digits=3, decimal_places=2, default=0.6)

    rem = models.DecimalField(max_digits=3, decimal_places=2, default=0.15)
    deep = models.DecimalField(max_digits=3, decimal_places=2, default=0.2)
    resting_heart_rate = models.DecimalField(max_digits=3, decimal_places=2, default=0.8)
    
    def __str__(self):
        return '%s "sleep"' % (self.date)


    def get_sleep_score(self):
        duration = float(self.duration)
        rem = float(self.rem)
        deep = float(self.deep)
        restfulness = float(self.restfulness)
        resting_heart_rate = float(self.resting_heart_rate)
        efficiency = float(self.efficiency)
        latency = float(self.latency)
        """
        calculate sleep quality score based on duration, percentage of REM, percentage of deep, restfulness, resting heart
        rate, sleep efficiency and sleep latency.

        :param duration: sleep duration in minutes
        :param rem: percentage of sleep being rem sleep
        :param deep: percentage of sleep being deep sleep
        :param restfulness: percentage
        :param resting_heart_rate: percentage
        :param efficiency: percentage
        :param latency: minutes
        :return: sleep quality score
        """
        if duration > 0:
            duration_quality = 1 + math.log(1 - (abs(duration/(9 * 60) - 1)))
            rem_quality = rem * 2 + 0.5 if rem > 0.2 else rem * 6 - 0.3 if rem > 0.15 else rem * 12 - 1.2 if rem > 1 else rem / 0.1 - 1
            deep_quality = -2 * (1 + math.exp(10 * deep - 0.375)) ** -1 + 1
            latency_quality = 1 + abs(latency - 15)/15
            return (duration_quality + rem_quality + deep_quality + restfulness + resting_heart_rate + efficiency +
                    latency_quality) / sum([1 for i in [duration, rem, deep, restfulness, resting_heart_rate, efficiency,
                                                        latency] if i])
        return 0


class Sleep_helper(models.Model):

    nap_start = models.DateTimeField()
    nap_end = models.DateTimeField()
    light = models.DecimalField(max_digits=3, decimal_places=2)
    caffeine = models.BooleanField(default=False)
    melatonin = models.BooleanField(default=False)

    # def __str__(self):
    #     return '%s %s %s' % (self.user, self.game, self.score)
    
    









