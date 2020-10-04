from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404
from schedule.models import Sleep_schedule
from sleep.models import Sleep


from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

today = date.today() 

# Create your views here.
def home_view(request, *args, **kwargs):
    # return HttpResponse('<h1>Home Page</h1>')

    # obj = Product.objects.get(id=id)
    date = today
    sleep_schedule = get_object_or_404(Sleep_schedule, date = today)
    
    schedule_date = sleep_schedule.date
    previous_date = schedule_date  - timedelta(days=1)
    next_date = schedule_date  + timedelta(days=1)
    
    sleep = Sleep.objects.filter(date=previous_date)


    # Date
    today_year = int(schedule_date.strftime('%Y'))
    today_month = int(schedule_date.strftime('%m'))
    today_date = int(schedule_date.strftime('%d'))

    tomorrow_year = int(next_date.strftime('%Y'))
    tomorrow_month = int(next_date.strftime('%m'))
    tomorrow_date = int(next_date.strftime('%d'))


    # Sleep time
    start_time = sleep_schedule.start_time
    end_time = sleep_schedule.end_time
    # Sleep hour/min
    sleep_start_hour = int(start_time.strftime("%H"))
    sleep_start_min = int(start_time.strftime("%M"))
    sleep_end_hour = int(end_time.strftime("%H"))
    sleep_end_min = int(end_time.strftime("%M"))

    # Nap or not
    take_nap = sleep_schedule.take_nap

    # Nap time
    nap_start = sleep_schedule.nap_start
    nap_end = sleep_schedule.nap_end
    # Nap hour/min
    if nap_start != None:
        nap_start_hour = int(nap_start.strftime("%H"))
        nap_start_min = int(nap_start.strftime("%M"))
        nap_end_hour = int(nap_end.strftime("%H"))
        nap_end_min = int(nap_end.strftime("%M"))
    else:
        nap_start_hour = 0
        nap_start_min = 0
        nap_end_hour = 0
        nap_end_min = 0


    # Breakfast time
    b_start = sleep_schedule.breakfast_start_time
    b_end = sleep_schedule.breakfast_end_time
    # Breakfast hour/min
    b_start_hour = int(b_start.strftime("%H"))
    b_start_min = int(b_start.strftime("%M"))
    b_end_hour = int(b_end.strftime("%H"))
    b_end_min = int(b_end.strftime("%M"))

    # Lunch time
    l_start = sleep_schedule.lunch_start_time
    l_end = sleep_schedule.lunch_end_time
    # Lunch hour/min
    l_start_hour = int(l_start.strftime("%H"))
    l_start_min = int(l_start.strftime("%M"))
    l_end_hour = int(l_end.strftime("%H"))
    l_end_min = int(l_end.strftime("%M"))

    # Dinner time
    d_start = sleep_schedule.dinner_start_time
    d_end = sleep_schedule.dinner_end_time
    # Dinner hour/min
    d_start_hour = int(d_start.strftime("%H"))
    d_start_min = int(d_start.strftime("%M"))
    d_end_hour = int(d_end.strftime("%H"))
    d_end_min = int(d_end.strftime("%M"))


    
    # aerobics_exercise time
    aerobics_exercise_start = sleep_schedule.aerobics_exercise_start
    aerobics_exercise_end = sleep_schedule.aerobics_exercise_end

    if aerobics_exercise_start != None:
    # aerobics_exercise_start hour/min
        aerobics_exercise_start_hour = int(aerobics_exercise_start.strftime("%H"))
        aerobics_exercise_start_min = int(aerobics_exercise_start.strftime("%M"))
        aerobics_exercise_end_hour = int(aerobics_exercise_end.strftime("%H"))
        aerobics_exercise_end_min = int(aerobics_exercise_end.strftime("%M"))
    else:
        aerobics_exercise_start_hour = 0
        aerobics_exercise_start_min = 0
        aerobics_exercise_end_hour = 0
        aerobics_exercise_end_min = 0



    # aerobics_exercise time
    resistant_excercise_start = sleep_schedule.resistant_excercise_start
    resistant_excercise_end = sleep_schedule.resistant_excercise_end
    if resistant_excercise_start != None:
        # aerobics_exercise_start hour/min
        resistant_excercise_start_hour = int(resistant_excercise_start.strftime("%H"))
        resistant_excercise_start_min = int(resistant_excercise_start.strftime("%M"))
        resistant_excercise_end_hour = int(resistant_excercise_end.strftime("%H"))
        resistant_excercise_end_min = int(resistant_excercise_end.strftime("%M"))
    else:
        resistant_excercise_start_hour = 0
        resistant_excercise_start_min = 0
        resistant_excercise_end_hour = 0
        resistant_excercise_end_min = 0

    # sleep helpers
    take_meditation = sleep_schedule.take_meditation
    take_melatonin = sleep_schedule.take_melatonin
    take_caffeine = sleep_schedule.take_caffeine

    # Scores
    sleep_score = sleep_schedule.sensed_score
    yesterday_PSQI_score = sleep_schedule.PSQI_score

    # Exercise or not
    do_resistant = sleep_schedule.do_resistant
    do_aerobics = sleep_schedule.do_aerobics



    # games = Game.objects.filter(end_time__gte = current_time).order_by('start_time') #list of object
    
    context = {

        'schedule':sleep_schedule,

        'schedule_date': schedule_date,
        'today_year':today_year,
        'today_month':today_month, 
        'today_date':today_date,
        'tomorrow_year': tomorrow_year, 
        'tomorrow_month': tomorrow_month,
        'tomorrow_date': tomorrow_date,

        'sleep_start_hour': sleep_start_hour,
        'sleep_start_min': sleep_start_min,
        'sleep_end_hour': sleep_end_hour,
        'sleep_end_min': sleep_end_min,

        'take_nap':take_nap,
        'nap_start_hour':nap_start_hour,
        'nap_start_min':nap_start_min,
        'nap_end_hour':nap_end_hour,
        'nap_end_min':nap_end_min,

        'b_start_hour':b_start_hour,
        'b_start_min': b_start_min,
        'b_end_hour':b_end_hour,
        'b_end_min':b_end_min,

        'l_start_hour': l_start_hour,
        'l_start_min':l_start_min,
        'l_end_hour':l_end_hour,
        'l_end_min':l_end_min,

        'd_start_hour': d_start_hour,
        'd_start_min':d_start_min,
        'd_end_hour':d_end_hour,
        'd_end_min':d_end_min,
    
        'aerobics_exercise_start_hour': aerobics_exercise_start_hour,
        'aerobics_exercise_start_min':aerobics_exercise_start_min,
        'aerobics_exercise_end_hour':aerobics_exercise_end_hour,
        'aerobics_exercise_end_min':aerobics_exercise_end_min,

        'resistant_excercise_start_hour': resistant_excercise_start_hour,
        'resistant_excercise_start_min':resistant_excercise_start_min,
        'resistant_excercise_end_hour':resistant_excercise_end_hour,
        'resistant_excercise_end_min':resistant_excercise_end_min,

        'take_meditation':take_meditation,
        'take_melatonin':take_melatonin,
        'take_caffeine':take_caffeine,

        'do_resistant':do_resistant,
        'do_aerobics':do_aerobics,


       
        'yesterday_PSQI_score': yesterday_PSQI_score,
        'sleep_score': sleep_score,

        'exercise':sleep_schedule.exercise,

        


    }
    return render(request, 'pages/home.html', context)





