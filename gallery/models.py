from django.db import models
from django.contrib.auth.models import User

class GalleryItem(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На перевірці'),
        ('approved', 'Схвалено'),
        ('rejected', 'Відхилено'),
    ]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='gallery/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def is_image(self):
        return self.file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))

    def is_video(self):
        return self.file.name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))

    def __str__(self):
        return self.title
