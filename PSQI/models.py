from django.db import models
import datetime
from datetime import date, timedelta
# Create your models here.

latency = 2
sleepDuration = 420
sleepEfficiency = 85


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
    INTENSITY= ( 
        ("1", "1"), 
        ("2", "2"), 
        ("3", "3"), 
        ("4", "4"), 
        ("5", "5"), 
        ("6", "6"), 
        ("7", "7"), 
        ("8", "8"), 
        ("9", "9"), 
        ("10", "10"), 
      
       
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

    userFeedBackIntensity = models.CharField(max_length = 20, choices = INTENSITY, default = '1', null = True, blank=True)

    day = models.IntegerField(default = 1, null= True, blank=True)



    def __str__(self):
        return '%s "PSQI"' % (self.date)

    
    def get_score(self, latency, sleepDuration, sleepEfficiency):        
        component = [0]*7;
        component[0] = int(self.selfRatedSleepQuality);
        
        #convert latency minutes to score
        if(latency <= 15):
            latency = 0;
        elif(latency < 30):
            latency = 1;
        elif(latency < 60):
            latency = 2;
        else:
            latency = 3;
            
        
        component[1] = latency+int(self.latencyGreaterThan30);
        #convert sum to score:
        if(component[1] == 0):
            component[1] = 0;
        elif(component[1] <= 2):
            component[1] = 1;
        elif(component[1] <= 4):
            component[1] = 2;
        else:
            component[1] = 3;
            
        component[2] = sleepDuration;
        if(component[2] > 420):
            component[2] = 0;
        elif(component[2] > 359):
            component[2] = 1;
        elif(component[2] > 299):
            component[2] = 2;
        else:
            component[2] = 3;
        
        component[3] = sleepEfficiency;
        if(component[3] > 85):
            component[3] = 0;
        elif(component[3] > 74):
            component[3]= 1;
        elif(component[3] > 64):
            component[3]= 2;
        else:
            component[3]= 3;
        
        
        component[4] = (int(self.midnightAwakeEarlyMorning) + int(self.useBathroom) + 
                        int(self.uncomfortableBreathing) + int(self.coughSnore) + int(self.feelCold) + 
                        int(self.feelHot) + int(self.badDreams) + int(self.pain) + int(self.otherReason))
        if(component[4] == 0):
            component[4] = 0;
        elif(component[4] <= 9):
            component[4]= 1;
        elif(component[4] <= 18):
            component[4]= 2;
        else:
            component[4]= 3;
        
        
        component[5] = int(self.sleepMedication);
        component[6] = int(self.stayAwakeDuringWork) + int(self.enthusiasmToDoThings);
        
        if(component[6] == 0):
            component[6] = 0;
        elif(component[6] <= 2):
            component[6] = 1;
        elif(component[6] <= 4):
            component[6] = 2;
        else:
            component[6] = 3;
            
        PSQI_score = sum(component);
        
        return PSQI_score





