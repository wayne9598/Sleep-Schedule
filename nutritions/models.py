from django.db import models
from django.db.models.signals import post_save
from schedule.models import Sleep_schedule
from exercises.models import Exercise
from sleep.models import Sleep
from datetime import date, timedelta


# Create your models here.
class Nutrition(models.Model):

    schedule = models.OneToOneField(Sleep_schedule, on_delete=models.CASCADE, null=True, blank=True)
    m_protein = models.FloatField()
    m_fat_saturated = models.FloatField()
    m_fat_unsaturated = models.FloatField()
    m_carb = models.FloatField()
    m_sugar = models.FloatField()
    m_NaCl = models.FloatField()
    m_potassium = models.FloatField()

    def __str__(self):
        return '%s Nutrution' % (self.schedule.date)

    def update_nutrition(self, m_protein, m_fat_saturated, m_fat_unsaturated, m_carb, m_sugar, m_NaCl, m_potassium):
        self.m_protein = m_protein
        self.m_fat_saturated = m_fat_saturated
        self.m_fat_unsaturated = m_fat_unsaturated
        self.m_carb = m_carb
        self.m_sugar = m_sugar
        self.m_NaCl = m_NaCl
        self.m_potassium = m_potassium

        self.save()
        

def create_nutrition(sender, instance, **kwargs):

    if kwargs['created']:
        print('schedule created!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(instance.astronaut)
        m_protein, m_fat_saturated, m_fat_unsaturated, m_carb, m_sugar, m_NaCl, m_potassium = calculate_nutrition_values(instance)
        
        nutrition = Nutrition.objects.create(
            schedule = instance,
            m_protein = m_protein,
            m_fat_saturated = m_fat_saturated,
            m_fat_unsaturated = m_fat_unsaturated,
            m_carb = m_carb,
            m_sugar = m_sugar,
            m_NaCl = m_NaCl,
            m_potassium = m_potassium,
        )

        exercise = Exercise.objects.create(
            date = instance.date
        )

        previous_date = instance.date  - timedelta(days=1)

        sleep = Sleep.objects.create(
            date = previous_date
        )
    
    else:
        print('updateeeeeeeeeeeeeeeeeeeeeeeeee')
        m_protein, m_fat_saturated, m_fat_unsaturated, m_carb, m_sugar, m_NaCl, m_potassium = calculate_nutrition_values(instance)
        instance.nutrition.update_nutrition(m_protein, m_fat_saturated, m_fat_unsaturated, m_carb, m_sugar, m_NaCl, m_potassium)
    




def calculate_nutrition_values(schedule):

    astronaut = schedule.astronaut
    sleepHrs = float(schedule.get_sleep_duration())
    exerciseHrs = float(schedule.get_exercise_hour())
    lightWorkHrs = float(schedule.light_work_hrs)
    heavyWorkHrs = float(schedule.heavy_work_hrs)
    mealHrs = float(schedule.get_meal_hour())
    weight = float(astronaut.weight)


    totalKCalConsumed = kCalConsumption(astronaut.gender, astronaut.age, weight, sleepHrs, exerciseHrs, lightWorkHrs, heavyWorkHrs, mealHrs)
    
    if(exerciseHrs != 0):
        m_protein = 1.6*weight
        E_protein = m_protein*4 #intake = 1.6 g/kg, energy = 4 KCal/g_protein
    else:
        m_protein = 1.2*weight
        E_protein = m_protein*4
    
    E_apartFromProtein = totalKCalConsumed-E_protein; #this should make up to 22.5%+55%+5%
    
    E_fat = ((22.5)/88)*E_apartFromProtein
    m_fat = E_fat/9; # energy = 9Kcal/g_fat
    
    E_carb = ((62.5)/88)*E_apartFromProtein
    m_carb = E_carb/4; # energy = 4Kcal/g_carbohydrate
    
    E_sugar = ((3)/88)*E_apartFromProtein
    m_sugar = E_sugar/4; # energy = 4Kcal/g_carbohydrate(sugar)
    
    m_fat_saturated = ((5)/88)*E_apartFromProtein/9; #5% of fats are saturated
    m_fat_unsaturated = m_fat-m_fat_saturated
    
    m_NaCl = 4; #<5 grams of salt
    mol_Na = (2/5*4)/23; #sodium molar mass = 23 where Na:NaCl = 2:5; 4 is from 4 g of NaCl
    m_potassium = mol_Na*39; # Na:K = 1:1, potassium molar mass = 39
    potassium = m_potassium

    return m_protein, m_fat_saturated, m_fat_unsaturated, m_carb, m_sugar, m_NaCl, m_potassium






def kCalConsumption(gender, age, weight, sleepHrs, exerciseHrs, lightWorkHrs, heavyWorkHrs, mealHrs):
        
        hrsADay = sleepHrs + exerciseHrs + lightWorkHrs + heavyWorkHrs + mealHrs;

        leisureHrs = 24-hrsADay; #if time doesn't add up to 24 than put energy consumption to low boundary
            
        if(gender == 'Male'):
            if (age <= 30):
                BMR = 15.057*weight+692.2;
            elif(age > 30):
                BMR = 11.472*weight+873.1;
            
                
            #PAR values for energy consumption, source from WHO & ucl.ac.uk/~ucbcdab/enbalance/definitions.htm
            PAR_exercise = 6.96; #circuit training
            PAR_lightWork = 1.3; #WHO office worker
            PAR_heavyWork = 3.0; #UCl
            PAR_meal = 1.4; #WHO
            PAR_leisure = 1.4; #WHO
            
            
        else:
            if (age <= 30):
                BMR = 14.818*weight+486.6;
            elif(age > 30):
                BMR = 8.126*weight+845.6;
            
                
            #PAR values for energy consumption, source from WHO & ucl.ac.uk/~ucbcdab/enbalance/definitions.htm
            PAR_exercise = 6.29; #circuit training
            PAR_lightWork = 1.5; #WHO office worker
            PAR_heavyWork = 2.3; #UCL
            PAR_meal = 1.6; #WHO
            PAR_leisure = 1.4; #WHO
        
        PAR_sleep = 1
        #PAL calculation
        PAL = (PAR_sleep*sleepHrs+PAR_exercise*exerciseHrs+PAR_lightWork*lightWorkHrs+
               PAR_heavyWork*heavyWorkHrs+PAR_meal*mealHrs+PAR_leisure*leisureHrs)/24;
        
        totalKCalConsumed = BMR*PAL; #total consumt
        
        return totalKCalConsumed;








post_save.connect(create_nutrition, sender = Sleep_schedule)
