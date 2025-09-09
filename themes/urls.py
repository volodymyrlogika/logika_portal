from django.urls import path
from .views import (
    ThemeListView, ThemeDetailView, ThemeCreateView,
    ThemeUpdateView, ThemeDeleteView, set_theme
)

app_name = "themes"

urlpatterns = [
    path("", ThemeListView.as_view(), name="theme_list"),

    # API endpoint — ставимо вище slug'ів
    path("set/", set_theme, name="set_theme"),

    # CRUD
    path("create/", ThemeCreateView.as_view(), name="theme_create"),
    path("<slug:slug>/update/", ThemeUpdateView.as_view(), name="theme_update"),
    path("<slug:slug>/delete/", ThemeDeleteView.as_view(), name="theme_delete"),
    path("<slug:slug>/", ThemeDetailView.as_view(), name="theme_detail"),
]
