import mimetypes
from django.db import models
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class GalleryItem(models.Model):
    file = models.FileField(upload_to='gallery/', null=True, blank=True)
    title = models.CharField(max_length=255)
    caption = models.CharField(max_length=500, blank=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def media_type(self):
        type, _ = mimetypes.guess_type(self.file.url)
        if type:
            if type.startswith('image'):
                return 'image'
            elif type.startswith('video'):
                return 'video'
        return 'other'

    def is_image(self):
        type, _ = mimetypes.guess_type(self.file.url)
        return type and type.startswith('image')

    def is_video(self):
        type, _ = mimetypes.guess_type(self.file.url)
        return type and type.startswith('video')
