from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    DeleteView,
)

# Create your views here.
def home_view(request, *args, **kwargs):
    # return HttpResponse('<h1>Home Page</h1>')
    return render(request, "pages/home.html", {})



