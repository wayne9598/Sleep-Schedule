from django.shortcuts import render
from .forms import PSQI_form

# Create your views here.


def PSQI_create_view(request):
    form = PSQI_form(request.POST or None)
    if form.is_valid():
        form.save()

    context = {
        'form':form
    }
 
    return render(request, 'PSQI/PSQI_create.html', context)