from django.urls import path, include

from .views import schedule_list_view, dynamic_schedule_lookup_view

app_name = 'schedule'
urlpatterns = [
    path('/list', schedule_list_view, name='schedule_list'),
    path('<int:id>', dynamic_schedule_lookup_view, name='schedule_detail'),

]

