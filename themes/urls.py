# themes/urls.py
from django.urls import path
from .views import (
    ThemeListView, ThemeDetailView,
    ThemeCreateView, ThemeUpdateView, ThemeDeleteView,
    switch_theme, set_theme
)
from . import views
app_name = "themes"

urlpatterns = [
    # список
    path("", ThemeListView.as_view(), name="theme_list"),
 
    
    # CRUD (порядок важливий!)
    path("create/", ThemeCreateView.as_view(), name="theme_create"),
    path("<slug:slug>/update/", ThemeUpdateView.as_view(), name="theme_update"),
    path("<slug:slug>/delete/", ThemeDeleteView.as_view(), name="theme_delete"),
    path("<slug:slug>/", ThemeDetailView.as_view(), name="theme_detail"),
    # перемикання теми
    path("set-theme/", set_theme, name="set_theme"),
]
