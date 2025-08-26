from django.db import models

class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва теми")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    background_color = models.CharField(max_length=7, default="#ffffff", verbose_name="Колір фону")
    text_color = models.CharField(max_length=7, default="#000000", verbose_name="Колір тексту")
    custom_css = models.TextField(blank=True, null=True, verbose_name="Кастомний CSS")

    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    MEDIA_TYPES = [
        ("image", "Фото"),
        ("video", "Відео"),
    ]

    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="gallery_items")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    file = models.FileField(upload_to="gallery/", verbose_name="Файл")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default="image", verbose_name="Тип медіа")
    approved = models.BooleanField(default=False, verbose_name="Схвалено")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
