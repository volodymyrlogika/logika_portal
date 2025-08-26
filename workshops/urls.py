from django.urls import path
from . import views

app_name = 'workshops'

urlpatterns = [
    # головна сторінка воркшопів
    path('', views.WorkshopListView.as_view(), name='home'),

    # Workshops CRUD
    path('new/', views.WorkshopCreateView.as_view(), name='workshop_create'),
    path('<slug:slug>/', views.WorkshopDetailView.as_view(), name='workshop_detail'),
    path('<int:pk>/edit/', views.WorkshopUpdateView.as_view(), name='workshop_edit'),
    path('<int:pk>/delete/', views.WorkshopDeleteView.as_view(), name='workshop_delete'),
]
