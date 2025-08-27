from django.urls import path
from .views import workshop_page

app_name = "workshops"

urlpatterns = [
    path("", workshop_page, name="page"),
]
