from django.shortcuts import render
from .models import Astronaut

# Create your views here.
def astronaut_view(request, *args, **kwargs):
    
    astronaut = Astronaut.objects.get()

    context = {
        'astronaut':astronaut
    }



    return render(request, "astronauts/profile.html", context)
