from django.db import models
from django.contrib.auth.models import User


from django.utils.text import slugify

class Theme(models.Model):
    name = models.CharField('Назва', max_length=120, unique=True)
    slug = models.SlugField('Слаг', max_length=140, unique=True, blank=True, null=True)
    description = models.TextField('Опис', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="themes")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class GalleryItem(models.Model):
    MEDIA_CHOICES = (
        ('image', 'Зображення'),
        ('video', 'Відео'),
        ('file', 'Файл'),
    )
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Опис', blank=True)
    file = models.FileField('Файл', upload_to="gallery/")
    media_type = models.CharField('Тип медіа', max_length=10, choices=MEDIA_CHOICES, default='image')
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gallery_items")
    workshop = models.ForeignKey("Workshop", on_delete=models.SET_NULL, null=True, blank=True, related_name="gallery_items")
    theme = models.ForeignKey("Theme", on_delete=models.SET_NULL, null=True, blank=True, related_name="gallery_items")
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Workshop(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True, related_name='workshops')
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workshops")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
