from django.shortcuts import render
from themes.models import Theme   # імпортуємо твою модель

def page(request):
    return render(request, "workshops/page.html")
def workshop_page(request):
    return render(request, "workshops/page.html")