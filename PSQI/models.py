from django.db import models
import datetime
from datetime import date, timedelta
# Create your models here.


class PSQI(models.Model):

    Q9_CHOICES = ( 
        ("0", "VeryGood"), 
        ("1", "FairlyGood"), 
        ("2", "FairlyBad"), 
        ("3", "VeryBad"), 
       
    )

    Q567_CHOICES = ( 
        ("0", "notDuringPastMonth"), 
        ("1", "lessThanOnceAWeek"), 
        ("2", "onceTwiceAWeek"), 
        ("3", "greaterThan3Aweek"), 
       
    )
    
    Q8_CHOICES = ( 
        ("0", "noProblem"), 
        ("1", "slightProblem"), 
        ("2", "someWhatAProblem"), 
        ("3", "bigProblem"), 
       
    )


    date = models.DateField(default = date.today() - timedelta(days=1))

    latencyGreaterThan30 = models.CharField(max_length = 20, choices = Q567_CHOICES, default = '1')  #5a
    midnightAwakeEarlyMorning = models.CharField(max_length = 20, choices = Q567_CHOICES, default = '1')  #5b
    useBathroom = models.CharField(max_length = 20, choices = Q567_CHOICES, default = '1')  #5c
    uncomfortableBreathing = models.CharField(max_length = 20, choices = Q567_CHOICES, default = '1')  #5d
    coughSnore = models.CharField(max_length = 20, choices = Q567_CHOICES, default = '1')  #5e
    feelCold = models.CharField(max_length = 20, choices = Q567_CHOICES, default = '1')  #5f
    feelHot = models.CharField(max_length = 20, choices = Q567_CHOICES, default = '1')  #5g
    badDreams = models.CharField(max_length = 20, choices = Q567_CHOICES, default = '1')  #5h
    pain = models.CharField(max_length = 20, choices = Q567_CHOICES, default = '1')  #5i
    otherReason = models.CharField(max_length = 20, choices = Q567_CHOICES, default = '1')  #5j
    sleepMedication = models.CharField(max_length = 20, choices = Q567_CHOICES, default = '1')  #6
    stayAwakeDuringWork = models.CharField(max_length = 20, choices = Q567_CHOICES, default = '1')  #7
    enthusiasmToDoThings = models.CharField(max_length = 20, choices = Q8_CHOICES, default = '1')  #8
    selfRatedSleepQuality = models.CharField(max_length = 20, choices = Q9_CHOICES, default = '1')  #9

    


   

    def __str__(self):
        return '%s "PSQI"' % (self.date)