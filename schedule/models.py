from django.db import models
from PSQI.models import PSQI
from django.utils import timezone
from datetime import date, timedelta



from django.db.models.signals import post_save


# Create your models here.
class Sleep_schedule(models.Model):
    date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    nap_start = models.DateTimeField(blank=True, null=True)
    nap_end = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '%s "sleep schedule"' % (self.date)



date = date.today() + timedelta(days=7)
start_time = timezone.now()
end_time = timezone.now()
nap_start = timezone.now()
nap_end = timezone.now()

## todo:


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


updated_start_time = timezone.now()
updated_end_time = timezone.now()
updated_nap_start = timezone.now()
updated_nap_end = timezone.now()





# Once submit PSQI, automatically update today's schedule based on PSQI and sensor data
def update_schedule(sender, **kwargs):
    if kwargs['created']:

        today_schedule = Sleep_schedule.objects.filter(date=date.today())[0].update(
            start_time = updated_start_time,
            end_time = updated_end_time,
            nap_start = updated_nap_start,
            nap_end = updated_nap_end,
        )
        


post_save.connect(create_schedule, sender = PSQI)
post_save.connect(update_schedule, sender = PSQI)


