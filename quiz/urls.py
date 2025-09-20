from django.urls import path
from . import views

urlpatterns = [
    path("quiz/<int:quiz_id>/", views.take_quiz, name="take_quiz"),
    path("quiz/<int:quiz_id>/result/", views.quiz_result, name="quiz_result"),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('create_quiz/', views.create_quiz, name='create_quiz'),
    path('create_question/', views.create_question, name='create_question'),
    path('create_answer/', views.create_answer, name='create_answer'),
    path('quiz_admin/', views.quiz_admin_panel, name='quiz_admin')
]
