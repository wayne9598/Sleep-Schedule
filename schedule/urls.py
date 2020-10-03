from django.urls import path, include

from .views import sleep_schedule_view

app_name = 'schedule'
urlpatterns = [
    path('', sleep_schedule_view, name='schedule'),
    

]

