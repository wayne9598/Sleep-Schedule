from django.urls import path, include
from .views import astronaut_view


app_name = 'astronauts'
urlpatterns = [
    path('/', astronaut_view, name='astronaut_view'),
    

]