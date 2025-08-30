from django.urls import path
from .views import workshop_page
from . import views
app_name = "workshops"

urlpatterns = [
    path("", workshop_page, name="page"),
    path("page/", views.page, name="page"),
]
