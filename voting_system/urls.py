from django.urls import path
from . import views
from .views import create_voting

urlpatterns = [
    path('', views.VoteListView.as_view(), name='vote-list'),
    path('<int:pk>/', views.VoteDetailView.as_view(), name ='voting-detail'),
    path('<int:pk>/delete/', views.VoteDeleteView.as_view(), name ='vote-delete'),
    path('voting-create/', create_voting, name='vote-create'),
]