from django.urls import path
from . import views

app_name = 'workshops'

urlpatterns = [
    # Themes
    path('themes/', views.ThemeListView.as_view(), name='theme_list'),
    path('themes/new/', views.ThemeCreateView.as_view(), name='theme_create'),
    path('themes/<int:pk>/edit/', views.ThemeUpdateView.as_view(), name='theme_edit'),
    path('themes/<int:pk>/delete/', views.ThemeDeleteView.as_view(), name='theme_delete'),

    # Workshops
    path('workshops/', views.WorkshopListView.as_view(), name='workshop_list'),
    path('workshops/new/', views.WorkshopCreateView.as_view(), name='workshop_create'),
    path('workshops/<slug:slug>/', views.WorkshopDetailView.as_view(), name='workshop_detail'),
    path('workshops/<int:pk>/edit/', views.WorkshopUpdateView.as_view(), name='workshop_edit'),
    path('workshops/<int:pk>/delete/', views.WorkshopDeleteView.as_view(), name='workshop_delete'),

    # Gallery
    path('gallery/', views.GalleryListView.as_view(), name='gallery_list'),
    path('gallery/upload/', views.GalleryCreateView.as_view(), name='gallery_upload'),
    path('gallery/moderation/', views.GalleryModerationListView.as_view(), name='gallery_moderation'),
    path('gallery/moderation/<int:pk>/approve/', views.approve_gallery_item, name='gallery_approve'),
    path('gallery/moderation/<int:pk>/delete/', views.delete_gallery_item, name='gallery_delete'),
]
