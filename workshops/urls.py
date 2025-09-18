from django.urls import path
from .views import WorkshopListView, WorkshopDetailView, WorkshopCreateView, publish_workshop
from . import views

app_name = "workshops"

urlpatterns = [
    path("", views.WorkshopListView.as_view(), name="list"),
    path("<slug:slug>/", views.WorkshopDetailView.as_view(), name="detail"),
    path("create/", views.WorkshopCreateView.as_view(), name="create"),
    path("<slug:slug>/update/", views.WorkshopUpdateView.as_view(), name="update"),  # 👈
    path("<slug:slug>/delete/", views.WorkshopDeleteView.as_view(), name="delete"),  # 👈
    path("<int:pk>/publish/", views.publish_workshop, name="publish"),   
]
