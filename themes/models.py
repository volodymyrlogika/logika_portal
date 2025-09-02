import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# ==============================
# ТЕМИ
# ==============================
from django.utils.text import slugify

class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    background_color = models.CharField(max_length=7, default="#ffffff")
    text_color = models.CharField(max_length=7, default="#000000")
    background_image = models.ImageField(upload_to="themes/backgrounds/", blank=True, null=True)
    font_family = models.CharField(max_length=50, blank=True)
    custom_css = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, default="")

    # Основні стилі
    background_color = models.CharField("Колір фону", max_length=7, default="#ffffff")
    text_color = models.CharField("Колір тексту", max_length=7, default="#000000")
    background_image = models.ImageField(
        "Фонове зображення", upload_to="themes/backgrounds/", blank=True, null=True
    )
    font_family = models.CharField(
        "Шрифт",
        max_length=100,
        choices=[
            ("Arial", "Arial"),
            ("Verdana", "Verdana"),
            ("Times New Roman", "Times New Roman"),
            ("Courier New", "Courier New"),
        ],
        default="Arial",
    )
    custom_css = models.TextField("Кастомний CSS", blank=True)

    # Додаткові поля
    is_active = models.BooleanField(default=False, verbose_name="Активна тема")
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="themes"
    )
    css_file = models.FileField(upload_to="themes/css/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)
        # Автоматичний slug
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

        # Генерація CSS при першому збереженні
        if not self.css_file:
            css_content = f"""
            /* Автоматично створений CSS для теми: {self.name} */
            body {{
                background-color: {"#fff" if "light" in self.name.lower() else "#121212"};
                color: {"#000" if "light" in self.name.lower() else "#eee"};
                font-family: {self.font_family}, sans-serif;
            }}
            .navbar {{
                background-color: {"#f8f9fa" if "light" in self.name.lower() else "#1f1f1f"};
            }}
            a {{
                color: {"#007bff" if "light" in self.name.lower() else "#66b2ff"};
            }}
            """
            filename = f"{self.slug or self.id}.css"
            self.css_file.save(filename, ContentFile(css_content.strip()), save=True)

    def __str__(self):
        return self.name


# ==============================
# ГАЛЕРЕЯ
# ==============================
class GalleryItem(models.Model):
    MEDIA_CHOICES = (
        ('image', 'Зображення'),
        ('video', 'Відео'),
        ('file', 'Файл'),
    )

    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Опис', blank=True)
    file = models.FileField('Файл', upload_to="gallery/")
    media_type = models.CharField(
        'Тип медіа', max_length=10, choices=MEDIA_CHOICES, default='image'
    )

    uploader = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="gallery_items"
    )
    workshop = models.ForeignKey(
        "Workshop", on_delete=models.SET_NULL, null=True, blank=True, related_name="gallery_items"
    )
    theme = models.ForeignKey(
        "Theme", on_delete=models.SET_NULL, null=True, blank=True, related_name="gallery_items"
    )

    approved = models.BooleanField(default=False, verbose_name="Схвалено")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ==============================
# ВОРКШОПИ
# ==============================
class Workshop(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва")
    description = models.TextField(blank=True, verbose_name="Опис")
    start_at = models.DateTimeField(null=True, blank=True, verbose_name="Початок")
    end_at = models.DateTimeField(null=True, blank=True, verbose_name="Кінець")
    location = models.CharField(max_length=200, blank=True, verbose_name="Локація")
    capacity = models.PositiveIntegerField(null=True, blank=True, verbose_name="Місткість")

    theme = models.ForeignKey(
        Theme, on_delete=models.SET_NULL, null=True, blank=True, related_name='workshops'
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубліковано")

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="workshops"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
