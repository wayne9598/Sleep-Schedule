from django.contrib import admin

# Register your models here.

from .models import Astronaut

admin.site.register(Astronaut)