from django.urls import path
from .views import (
    ThemeListView, ThemeDetailView,
    ThemeCreateView, ThemeUpdateView, ThemeDeleteView,
     set_theme
)

app_name = "themes"

urlpatterns = [
    # список усіх тем
    path("", ThemeListView.as_view(), name="list"),
    path("new/", ThemeCreateView.as_view(), name="create"),

    # деталі теми
    path("<int:pk>/", ThemeDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", ThemeUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", ThemeDeleteView.as_view(), name="delete"),

    # застосування теми
    path("<int:theme_id>/set/", set_theme, name="set"),
    path("<int:theme_id>/apply/", set_theme, name="apply"),
]
