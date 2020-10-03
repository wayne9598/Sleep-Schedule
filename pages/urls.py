from django.urls import path, include
# from . import views
from .views import home_view

app_name = 'pages'
urlpatterns = [
    path('', home_view, name='home'),
    

]