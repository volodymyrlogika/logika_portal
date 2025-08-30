from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    name = models.TextField(max_length=200, verbose_name="Ім'я тестування")
    discription = models.CharField(null=True, blank=True, verbose_name="Опис")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Створенно: ")

    def __str__(self):
        return self.name

class Question(models.Model):
    question = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="Запитання")
    text = models.TextField(max_length=250, verbose_name='Текст')
    page_number = models.PositiveIntegerField(default=1, verbose_name="Сторінка питання")

    def __str__(self):
        return f"{self.survey.title} - {self.text}"
    
class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options", verbose_name="Запитання")
    text = models.CharField(max_length=255, verbose_name="Відповідь")

    def __str__(self):
        return self.text
    
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    survey = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="Тестування")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Питання")
    selected_option = models.ForeignKey(AnswerOption, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Вибранна відповідь")
    text_answer = models.TextField(blank=True, null=True, verbose_name="Відповідь користувача")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        unique_together = ('user', 'survey', 'question')