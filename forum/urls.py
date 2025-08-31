from django.urls import path
from . import views

urlpatterns = [
   
    path('categories/', views.AllCategoryListView.as_view()),
    path('threads/', views.AllThreadListView.as_view()),
    path('home/', views.ForumHomeView.as_view()),

]
