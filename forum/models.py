from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('games', 'Ігри'),
        ('code', 'Програмування'),
        ('music', 'Музика'),
        ('sport', 'Спорт'),
        ('other', 'Інше'),
        ]
    
    name = models.CharField(max_length=256)
    description = models.TextField()
    type = models.CharField(max_length=35, choices=CATEGORY_TYPE_CHOICES)


class Thread(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="branches")


class Post(models.Model):
    branch = models.ForeignKey(Thread, on_delete=models.CASCADE)