# Create your models here.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# from prizes.models import Prize


# Create your models here.
class Sleep(models.Model):
    date = models.DateField()

    total_sleep_time = models.IntegerField()
    efficiency = models.DecimalField(max_digits=3, decimal_places=2)
    start_time = models.TimeField()
    end_time = models.TimeField()
    latency = models.IntegerField()
    body_temperature = models.IntegerField()
    # Restfulness = wake/total sleep
    restfulness = models.DecimalField(max_digits=3, decimal_places=2)

    REM = models.DecimalField(max_digits=3, decimal_places=2)
    deep_sleep = models.DecimalField(max_digits=3, decimal_places=2)
    average_resting_heart_rate = models.IntegerField()

    def __str__(self):
        return '%s "sleep"' % (self.date)


class Sleep_helper(models.Model):

    nap_start = models.DateTimeField()
    nap_end = models.DateTimeField()
    light = models.DecimalField(max_digits=3, decimal_places=2)
    caffeine = models.BooleanField(default=False)
    melatonin = models.BooleanField(default=False)

    # def __str__(self):
    #     return '%s %s %s' % (self.user, self.game, self.score)
    
    









