from django.urls import path
from .views import (
    AnnouncementListView, AnnouncementDetailView,
    AnnouncementCreateView, AnnouncementUpdateView, AnnouncementDeleteView
)

urlpatterns = [
    path("", AnnouncementListView.as_view(), name="announcement_list"),
    path("<int:pk>/", AnnouncementDetailView.as_view(), name="announcement_detail"),
    path("create/", AnnouncementCreateView.as_view(), name="announcement_create"),
    path("<int:pk>/edit/", AnnouncementUpdateView.as_view(), name="announcement_edit"),
    path("<int:pk>/delete/", AnnouncementDeleteView.as_view(), name="announcement_delete"),
]
