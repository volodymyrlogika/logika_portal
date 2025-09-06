# themes/urls.py
from django.urls import path
from .views import (
    ThemeListView, ThemeDetailView,
    ThemeCreateView, ThemeUpdateView, ThemeDeleteView,
    theme_switch, set_theme
)
from . import views
app_name = "themes"

urlpatterns = [
    path("", ThemeListView.as_view(), name="theme_list"),

    # дії
    path("switch/", views.theme_switch, name="theme_switch"),
    path("set-theme/", views.set_theme, name="set_theme"),
    path("<int:pk>/apply/", views.apply_theme, name="apply"),
    path("create/", ThemeCreateView.as_view(), name="theme_create"),
    path("<slug:slug>/update/", ThemeUpdateView.as_view(), name="theme_update"),
    path("<slug:slug>/delete/", ThemeDeleteView.as_view(), name="theme_delete"),

    # деталі завжди останні
    path("<slug:slug>/", ThemeDetailView.as_view(), name="theme_detail"),
]

