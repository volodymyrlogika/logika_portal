from django.shortcuts import render
from themes.models import Theme   # імпортуємо твою модель

def workshop_page(request):
    themes = Theme.objects.all()   # беремо всі теми
    return render(request, "workshops/workshop_page.html", {"themes": themes})
