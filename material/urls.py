from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.material, name='material'),
    path('add/', views.add_material, name='add_material'),
    path('delete/<int:material_id>/', views.delet_material, name='delet_material'),
]
