from django.db import models
from django.contrib.auth.models import User

class Lesson(models.Model):
    title = models.CharField(max_length=100,verbose_name="Назва уроку")
    datetime = models.DateTimeField(verbose_name="Дата Уроку")

class Logik(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Учень") 
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,verbose_name="Урок")
    grade = models.IntegerField(verbose_name="Оцінка")           
    date_creation= models.DateTimeField(auto_now_add=True,verbose_name="Дата")