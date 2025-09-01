from django.urls import path
from . import views


urlpatterns = [
   
    path('categories/', views.AllCategoryListView.as_view(), name="categories"),
    path('all-threads/', views.AllThreadListView.as_view(), name="all-threads"),
    path('home/', views.ForumHomeView.as_view(), name="home"),
    path('category/<int:category_id>/thread/', views.ThreadListView.as_view(), name="thread-list"),
    path('category/<int:category_id>/thread/<int:thread_id>/', views.PostList.as_view(), name="post-list"),

]
app_name = 'forum'

