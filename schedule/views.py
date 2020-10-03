from django.shortcuts import render, get_object_or_404
from .models import Sleep_schedule
import datetime
from PSQI.models import PSQI
from datetime import date, timedelta


# Create your views here.

def sleep_schedule_view(request):
    
    # All games that are not ended yet
    # user_score = Score.objects.filter(user=user, game=game)
    date = datetime.datetime.now()
    sleep_schedule = Sleep_schedule.objects.filter(date=date)[0]

    # sleep_schedule = get_object_or_404(Sleep_schedule)
    schedule_date = sleep_schedule.date
    start_time = sleep_schedule.start_time
    end_time = sleep_schedule.end_time
    nap_start = sleep_schedule.nap_start
    nap_end = sleep_schedule.nap_end

    backgoundcolor = 'lightblue'

    # Data from sensors
    latency = 2
    sleepDuration = 420
    sleepEfficiency = 85

    # yesterday's PSQI
    yesterday = date.today() - timedelta(days=1)
    yesterday_PSQI = PSQI.objects.filter(date=yesterday)[0]
    yesterday_PSQI_score = yesterday_PSQI.get_score(latency, sleepDuration, sleepEfficiency)


    # games = Game.objects.filter(end_time__gte = current_time).order_by('start_time') #list of object
    
    context = {
        'schedule_date': schedule_date,
        'start_time':start_time,
        'end_time':end_time,
        'nap_start':nap_start,
        'nap_end':nap_end,
        'backgoundcolor':backgoundcolor,
        'yesterday_PSQI_score': yesterday_PSQI_score,

    }

    return render(request, 'schedule/schedule.html', context)






