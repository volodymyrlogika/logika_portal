from django.urls import path
from .views import WorkshopListView, WorkshopDetailView, WorkshopCreateView, publish_workshop


app_name = "workshops"

urlpatterns = [
    path("", WorkshopListView.as_view(), name="list"),
    path("create/", WorkshopCreateView.as_view(), name="create"),
    path("<slug:slug>/", WorkshopDetailView.as_view(), name="detail"),
    path("<int:pk>/publish/", publish_workshop, name="publish"),
]
