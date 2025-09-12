import mimetypes
from django.db import models
from django.contrib.auth.models import User
from taggit.forms import TagField
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    file = models.FileField(upload_to='gallery/', null=True, blank=True)
    title = models.CharField(max_length=255)
    caption = models.CharField(max_length=500, blank=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 🆕 нові поля
    tags = models.ManyToManyField(Tag, blank=True)
    AGE_CHOICES = [
        ("e", "Everyone"),
        ("t", "Teen"),
        ("m", "Mature"),
        ("a", "Adults Only"),
    ]
    age_rating = models.CharField(max_length=1, choices=AGE_CHOICES, default="e")

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
            elif type.startswith('audio'):
                return 'audio'
        return 'other'

    def is_image(self):
        return self.file and self.file.url.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))

    def is_gif(self):
        return self.file and self.file.url.lower().endswith(".gif")

    def is_video(self):
        return self.file and self.file.url.lower().endswith((".mp4", ".mov", ".avi", ".webm"))

    def is_audio(self):
        return self.file and self.file.url.lower().endswith((".mp3", ".wav", ".ogg"))
