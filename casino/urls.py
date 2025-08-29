from django.urls import path
from . import views

app_name = 'casino'

urlpatterns = [
    path('', views.casino_home, name='home'),
]
