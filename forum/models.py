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
    image = models.ImageField(upload_to="categories/", null=True, blank=True)
    def __str__(self):
        return self.name

class Thread(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="threads")
    theme = models.CharField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    date_start = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    image = models.ImageField(upload_to="Thread", null=True, blank=True)

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content_text = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    files = models.FileField(upload_to="posts/", null=True, blank=True)
