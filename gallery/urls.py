from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    # головна сторінка галереї
    path('', views.GalleryListView.as_view(), name='home'),

    # Gallery CRUD
    path('upload/', views.GalleryCreateView.as_view(), name='upload'),

    # Модерація
    path('moderation/', views.GalleryModerationListView.as_view(), name='moderation'),
    path('moderation/<int:pk>/approve/', views.approve_gallery_item, name='approve'),
    path('moderation/<int:pk>/delete/', views.delete_gallery_item, name='delete'),
]
