from django.db import models
from django.contrib.auth.models import User

class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст оголошення")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcements", verbose_name="Автор")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated = models.DateTimeField(auto_now=True, verbose_name="Оновлено")
    is_published = models.BooleanField(default=True, verbose_name="Опубліковано")

    class Meta:
        ordering = ["created"]
        verbose_name = "Оголошення"
        verbose_name_plural = "Оголошення"

    def __str__(self):
        return self.title


    
