from django.urls import path
from .views import (
    ThemeListView,
    ThemeDetailView,
    ThemeCreateView,
    ThemeUpdateView,
    ThemeDeleteView,
    set_theme,
    ThemeFromWorkshopCreateView,  # ✅ додав цей імпорт
)

app_name = "themes"

urlpatterns = [
    # список тем
    path("", ThemeListView.as_view(), name="theme_list"),

    # створення
    path("create/", ThemeCreateView.as_view(), name="theme_create"),

    # створення теми з воркшопа
    path(
        "add-from-workshop/<int:workshop_id>/",
        ThemeFromWorkshopCreateView.as_view(),
        name="add_from_workshop"
    ),

    # зміна активної теми через AJAX
    path("set/", set_theme, name="set_theme"),

    # редагування
    path("<slug:slug>/update/", ThemeUpdateView.as_view(), name="theme_update"),

    # видалення
    path("<slug:slug>/delete/", ThemeDeleteView.as_view(), name="theme_delete"),

    # деталі
    path("<slug:slug>/", ThemeDetailView.as_view(), name="theme_detail"),
]
