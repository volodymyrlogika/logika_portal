from django.urls import path
from . import views

app_name = "main"  # ✅ Додаємо app_name

urlpatterns = [
    path('', views.index, name='home'),  # головна сторінка
    # Додай тут свої маршрути, якщо потрібно
]
