from django.urls import path
from . import views

urlpatterns = [
    path('editor/', views.theme_create, name='theme_create'),
    path('workshop/', views.theme_list, name='theme_list'),
    path('delete/<int:pk>/', views.theme_delete, name='theme_delete'),
    path('test-theme/', views.test_theme, name='test_theme'),
]
