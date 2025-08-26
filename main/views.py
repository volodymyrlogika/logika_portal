from django.shortcuts import render
from workshops.models import Workshop

def home(request):
    return render(request, "base.html")

def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, "main.html")