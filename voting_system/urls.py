from django.urls import path
from . import views

urlpatterns = [
    path('', views.VoteListView.as_view(), name='vote-list'),
    path('<int:pk>/', views.VoteDetailView.as_view(), name ='voting-detail'),
    path('<int:pk>/delete/', views.VoteDeleteView.as_view(), name ='vote-delete'),
    path('voting-create/', views.VoteCreateView.as_view(), name='vote-create'),
]