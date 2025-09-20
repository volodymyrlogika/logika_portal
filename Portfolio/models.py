from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    screenshot = models.ImageField(upload_to='portfolio/images/')
    link = models.URLField(blank=True)
    file = models.FileField(blank=True, upload_to='portfolio/files/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user = self.user
        title = self.title
        link = self.link
        created_at = self.created_at

        
        return f"Назва: {title} Ссылка: {link}  Дата: {created_at} Автор: {user}"
    


# Create your models here.
  