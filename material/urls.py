from django.urls import path
from . import views

urlpatterns = [
   
    path('material/', views.material, name='material'),
    path('add_material/', views.add_material, name='add_material'),
    path('delet_material/<int:material_id>/', views.delet_material, name='delet_material'),
]
