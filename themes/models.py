import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User


class Theme(models.Model):
    css_file = models.FileField(upload_to="themes/css/", blank=True, null=True)
    name = models.CharField("Назва", max_length=120, unique=True)
    slug = models.SlugField("Слаг", max_length=140, unique=True, blank=True, null=True)
    description = models.TextField("Опис", blank=True)
    tags = models.CharField(max_length=255, blank=True)
    image = models.ImageField("Обкладинка", upload_to="themes/images/", blank=True, null=True)
    is_draft = models.BooleanField("Чернетка", default=False)
    publish_date = models.DateTimeField("Дата публікації", null=True, blank=True)
    priority = models.PositiveIntegerField("Пріоритет", default=1)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="themes",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Якщо не заданий автор → ставимо суперкористувача
        if not self.created_by_id:
            self.created_by = User.objects.filter(is_superuser=True).first()

        # Генеруємо slug
        if not self.slug:
            self.slug = slugify(self.name)

        # Зберігаємо базовий запис
        super().save(*args, **kwargs)

        # Якщо css_file ще не створений → генеруємо
        if not self.css_file:
            css_content = f"""
            /* Автоматично створений CSS для теми: {self.name} */
            body {{
                background-color: {"#fff" if "light" in self.name.lower() else "#121212"};
                color: {"#000" if "light" in self.name.lower() else "#eee"};
                font-family: Arial, sans-serif;
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
