from django.urls import path
from . import views

urlpatterns = [
   
    path('categories/', views.CategoryListView.as_view()),
    path('threads/', views.ThreadListView.as_view()),
    path('home/', views.ForumHomeView.as_view()),

]
