from django.shortcuts import render
from workshops.models import Workshop
from themes.models import Theme  
def home(request):
    return render(request, "base.html")

def index(request):
    if request.user.is_authenticated and hasattr(request.user, "profile"):
        theme = getattr(request.user.profile, "theme", None)
    else:
        theme = request.session.get("theme", "light")

    return render(request, "index.html", {"theme": theme})