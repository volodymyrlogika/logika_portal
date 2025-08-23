from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('calendar/', views.EventListView.as_view(), name='calendar'),
    path('calendar/create/', views.EventCreateView.as_view(), name='calendar-create'),
    path('calendar/update/<int:pk>/', views.EventUpdateView.as_view(), name='calendar-update'),
    path('calendar/delete/<int:pk>/', views.EventDeleteView.as_view(), name='calendar-delete'),

]