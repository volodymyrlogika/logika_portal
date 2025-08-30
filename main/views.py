from django.shortcuts import render
from workshops.models import Workshop
from themes.models import Theme  
def home(request):
    return render(request, "base.html")

def index(request):
    themes = Theme.objects.all()  # тепер без is_draft
    return render(request, "index.html", {"themes": themes})


