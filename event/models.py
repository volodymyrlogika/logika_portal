from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name='Назва події')
    description = models.TextField(null=True, blank=True, verbose_name='Опис події')
    date = models.DateField(verbose_name='Дата події')
    speciality = (
        ("-", 'none'),
        ('+-', "soso"),
        ('+', "indeed"),
        ('++', "VERY NEED")
    )
    speciality = models.CharField(choices=speciality, default="-", verbose_name='Важливість події')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Користувач')    