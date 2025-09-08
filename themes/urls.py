# themes/urls.py
from django.urls import path
from .views import (
    ThemeListView, ThemeDetailView,
    ThemeCreateView, ThemeUpdateView, ThemeDeleteView,
     set_theme, apply_theme
)
from . import views
app_name = "themes"

urlpatterns = [
    # список + створення
    path("", ThemeListView.as_view(), name="theme_list"),
    path("create/", ThemeCreateView.as_view(), name="theme_create"),

    # дії з темами
   
    path("set/", views.set_theme, name="set_theme"),
    path("<int:pk>/apply/", apply_theme, name="apply"),

    # редагування / видалення / перегляд
    path("<slug:slug>/update/", ThemeUpdateView.as_view(), name="theme_update"),
    path("<slug:slug>/delete/", ThemeDeleteView.as_view(), name="theme_delete"),
    path("<slug:slug>/", ThemeDetailView.as_view(), name="theme_detail"),
]
