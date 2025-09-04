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
    
    name = models.CharField(max_length=256, verbose_name="назва категорії")
    description = models.TextField(null=True, blank=True, verbose_name="опис категорії")
    type = models.CharField(max_length=35, choices=CATEGORY_TYPE_CHOICES)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)
    def __str__(self):
        return f"{self.name}  — {self.description[:10]}"

class Thread(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="threads")
    theme = models.CharField(max_length=300, verbose_name="тема обговорення")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True, verbose_name="опис")
    date_start = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    image = models.ImageField(upload_to="Thread", null=True, blank=True)

def __str__(self):
    return self.theme

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content_text = models.TextField(null=False, verbose_name="текст контенту")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата створення")
    files = models.FileField(upload_to="posts/", null=True, blank=True)

    url_thread_id = models.IntegerField(null=True, blank=True)
    url_category_id = models.IntegerField(null=True, blank=True)
