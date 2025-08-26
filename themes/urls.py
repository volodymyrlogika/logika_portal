from django.urls import path
from . import views

app_name = 'themes'

urlpatterns = [
    # головна сторінка тем
    path('', views.ThemeListView.as_view(), name='home'),

    # Themes CRUD
    path('new/', views.ThemeCreateView.as_view(), name='theme_create'),
    path('<int:pk>/edit/', views.ThemeUpdateView.as_view(), name='theme_edit'),
    path('<int:pk>/delete/', views.ThemeDeleteView.as_view(), name='theme_delete'),
]
