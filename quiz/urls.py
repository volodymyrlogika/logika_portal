from django.urls import path
from . import views

urlpatterns = [
    path("quiz/<int:quiz_id>/", views.take_quiz, name="take_quiz"),
    path("quiz/<int:quiz_id>/result/", views.quiz_result, name="quiz_result"),
]
