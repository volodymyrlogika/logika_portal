from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    name = models.TextField(max_length=200)
    discription = models.CharField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    question = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(max_length=250)
    page_number = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.survey.title} - {self.text}"
    
class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
    
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(AnswerOption, on_delete=models.SET_NULL, null=True, blank=True)
    text_answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'survey', 'question')