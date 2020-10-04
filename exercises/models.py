from django.db import models
from django.db.models.signals import post_save
from PSQI.models import PSQI
from datetime import date, timedelta
from sleep.models import Sleep



# Create your models here.
class Exercise(models.Model):

    PSQI = models.OneToOneField(PSQI, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    userFeedBackIntensity = models.IntegerField(default = 6)
    lastTargetIntensity = models.FloatField(default = 0)
    targetIntensity = models.FloatField(default=7)
    intensity = models.FloatField(null=True, blank=True)

    do_exercise = models.BooleanField(default = True, blank= True, null = True)
    ared_name = models.CharField(max_length=200, default='None')
    aero_name = models.CharField(max_length=200, default='None')

    aredTime = models.FloatField(null=True, blank=True)
    aerobicTime = models.FloatField(null=True, blank=True)
    load = models.FloatField(null=True, blank=True)
    



    def __str__(self):
        return '%s Exercise' % (self.date)
    
    def update(self, userFeedBackIntensity,lastTargetIntensity,targetIntensity, date, instance):

        intensity = PID_intensityCalculator(userFeedBackIntensity, lastTargetIntensity, targetIntensity)
        exercise_result = exercisePlanner(date, intensity)

        self.PSQI = instance

        self.userFeedBackIntensity = userFeedBackIntensity
        self.lastTargetIntensity = lastTargetIntensity
        self.targetIntensity = targetIntensity
        self.intensity = intensity

        if exercise_result[0] == 'rest':
            self.do_exercise = False
        else:
             # 0 - rest or non-rest
            # 1 - ared_name
            # 2 - aero_name
            # 3 - ared time
            # 4 - aero time
            # 5 - load

            self.ared_name = exercise_result[1] 
            self.aero_name = exercise_result[2] 

            self.aredTime = exercise_result[3] 
            self.aerobicTime = exercise_result[4] 
            self.load = exercise_result[5] 

        self.save()



# When schedule created --> create Excercise




# When PSQI submitted --> update exsercise --> update schedule --> nutrition
today = date.today() 

def update_excercise(sender, instance, **kwargs):
    if kwargs['created']:

       

        # previous_date = instance.date
        previous_date = instance.date - timedelta(days=1)
        today_excercise = Exercise.objects.filter(date=instance.date)[0]
        previous_day_excercise = Exercise.objects.filter(date=previous_date)


        if previous_day_excercise:
            previous_day_excercise = previous_day_excercise[0]

            userFeedBackIntensity = int(instance.userFeedBackIntensity)
            # userFeedBackIntensity = 1
            lastTargetIntensity = previous_day_excercise.targetIntensity

            targetIntensity = 8
            date = instance.day
            # date = 2
        # First Day
        else:
            userFeedBackIntensity = 6
            lastTargetIntensity = 7
            targetIntensity = 8
            date = 1
        
        today_excercise.update(userFeedBackIntensity,lastTargetIntensity,targetIntensity, date, instance)  

    


post_save.connect(update_excercise, sender = PSQI)





def PID_intensityCalculator(userFeedBackIntensity, lastTargetIntensity, targetIntensity):
    
    previousError = lastTargetIntensity - (userFeedBackIntensity/6)*lastTargetIntensity;
    error = targetIntensity - (userFeedBackIntensity/6)*targetIntensity;

    ku = 0.05;
    T_crit = 0.05; #critical period
    T = 1;
    kp = 0.6*ku; #constant for proportional controller
    ki = 0.5*T_crit; #constant for integral controller
    kd = 0.125*T_crit; #constant for differential controller
    scalingFactor = 1;

    iCon = 0

    pCon = error*kp;
    iCon = iCon + ki*(T/2)*(error+previousError);
    dCon = kd*(error-previousError)/T;
    pidCon = pCon + iCon + dCon;
    
    if (pidCon > scalingFactor):
        pidCon = scalingFactor;
    elif (pidCon < -scalingFactor):
        pidCon = -scalingFactor;
        
    intensity = targetIntensity + (10*(pidCon)/scalingFactor);
        
    if(lastTargetIntensity == 0): #if last target is not set
        intensity = targetIntensity;
    
    return intensity;


def exercisePlanner(date, intensity):

    result = ['rest',0,0,0,0,0]
    # 0 - rest or non-rest
    # 1 - ared_name
    # 2 - aero_name
    # 3 - ared time
    # 4 - aero time
    # 5 - load

    if (date < 2):
        result[0] = 'rest'

    elif(date < 7):
        periodicWorkout = date%3;
        #training cycle ergometer
        if(periodicWorkout == 0 and intensity <= 6):
            load = 0.5;
            aredTime = 0;
            aerobicTime = 0.6;
            result[0] = 'not-rest'
            result[1] = 'Cycle Ergometer'
            result[2] = 'rest'
            result[3] = aredTime
            result[4] = aerobicTime
            result[5] = load
          
        elif(periodicWorkout == 0 and intensity > 6):
            load = 0.6
            aredTime = 0;
            aerobicTime = 0;
            result[0] = 'not-rest'
            result[1] = 'Cycle Ergometer'
            result[2] = 'rest'
            result[3] = aredTime
            result[4] = aerobicTime
            result[5] = load

        #training ARED
        elif(periodicWorkout == 1 and intensity <= 6):
            load = 0.5;
            aredTime = 0;
            aerobicTime = 0.6;

            result[0] = 'not-rest'
            result[1] = 'rest'
            result[2] = 'Treadmill'
            result[3] = aredTime
            result[4] = aerobicTime
            result[5] = load

            
        elif(periodicWorkout == 1 and intensity > 6):
            load = 0.6;
            aredTime = 0;
            aerobicTime = 0.6;

            result[0] = 'not-rest'
            result[1] = 'rest'
            result[2] = 'Treadmill'
            result[3] = aredTime
            result[4] = aerobicTime
            result[5] = load


        elif(periodicWorkout == 2 and intensity <= 6):
            load = 0.5;
            aredTime = 0.6;
            aerobicTime = 0;

            result[0] = 'not-rest'
            result[1] = 'ARED'
            result[2] = 'rest'
            result[3] = aredTime
            result[4] = aerobicTime
            result[5] = load


        elif(periodicWorkout == 2 and intensity > 6):
            load = 0.6;
            aredTime = 0.6;
            aerobicTime = 0;

            result[0] = 'not-rest'
            result[1] = 'ARED'
            result[2] = 'rest'
            result[3] = aredTime
            result[4] = aerobicTime
            result[5] = load

       
    
    elif(date<14):
        periodicWorkout = date%3;
        if(periodicWorkout == 0):
            aredTime = 0.7;
            aerobicTime = 0.5;
            load = intensity/20+0.5;

            result[0] = 'not-rest'
            result[1] = 'ARED'
            result[2] = 'Cycle ergometer'
            result[3] = aredTime
            result[4] = aerobicTime
            result[5] = load


        elif(periodicWorkout == 1):
            aredTime = 0.7;
            aerobicTime = 0.5;
            load = intensity/20+0.5;

            result[0] = 'not-rest'
            result[1] = 'ARED'
            result[2] = 'Treadmill'
            result[3] = aredTime
            result[4] = aerobicTime
            result[5] = load


        elif(periodicWorkout == 2):
            aredTime = 0;
            aerobicTime = 0; 
            load = 0;
        
    elif(date<21):
        periodicWorkout = date%3;
        if(periodicWorkout == 0):
            aredTime = 1;
            aerobicTime = 0.5;
            load = intensity/20+0.5;

            result[0] = 'not-rest'
            result[1] = 'ARED'
            result[2] = 'Cycle ergometer'
            result[3] = aredTime
            result[4] = aerobicTime
            result[5] = load

       


        elif(periodicWorkout == 1):
            aredTime = 1;
            aerobicTime = 0.5;
            load = intensity/20+0.5;

            result[0] = 'not-rest'
            result[1] = 'ARED'
            result[2] = 'Treadmill'
            result[3] = aredTime
            result[4] = aerobicTime
            result[5] = load



        elif(periodicWorkout == 2):
            aredTime = 0;
            aerobicTime = 0; 
            load = 0;
        
    else:
        periodicWorkout = date%5;
        if(periodicWorkout == 1 or periodicWorkout == 3):
            aredTime = 1;
            aerobicTime = 0.5;
            load = intensity/20+0.5;


            result[0] = 'not-rest'
            result[1] = 'ARED'
            result[2] = 'Cycle Ergometer'
            result[3] = aredTime
            result[4] = aerobicTime
            result[5] = load

        elif(periodicWorkout == 2 or periodicWorkout == 5):
            aredTime = 1;
            aerobicTime = 0.5;
            load = intensity/20+0.5;

            result[0] = 'not-rest'
            result[1] = 'ARED'
            result[2] = 'Treadmill'
            result[3] = aredTime
            result[4] = aerobicTime
            result[5] = load

            
        elif(periodicWorkout == 4):
            aredTime = 0;
            aerobicTime = 0; 
            load = 0;

    return result    
