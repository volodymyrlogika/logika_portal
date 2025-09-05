from django.urls import path
from . import views

urlpatterns = [
    path('', views.VoteListView.as_view(), name='vote-list'),
    path('<int:pk>/', views.VoteDetailView.as_view(), name ='voting-detail'),
]