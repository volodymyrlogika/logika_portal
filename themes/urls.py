# themes/urls.py
from django.urls import path
from .views import (
    ThemeListView, ThemeDetailView,
    ThemeCreateView, ThemeUpdateView, ThemeDeleteView,
    switch_theme
)
from . import views
app_name = "themes"

urlpatterns = [
    # список і CRUD
    path("", ThemeListView.as_view(), name="list"),
    path("create/", ThemeCreateView.as_view(), name="create"),
    path("<slug:slug>/", ThemeDetailView.as_view(), name="detail"),
    path("<slug:slug>/update/", ThemeUpdateView.as_view(), name="update"),
    path("<slug:slug>/delete/", ThemeDeleteView.as_view(), name="delete"),

    # перемикання теми (POST)
    path("switch/<slug:slug>/", views.switch_theme, name="switch"),

]
