import time
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User


class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField("Опис", blank=True)

    background_color = models.CharField("Колір фону", max_length=7, default="#ffffff")
    

    background_image = models.ImageField(
        "Фонове зображення", upload_to="themes/backgrounds/", blank=True, null=True
    )

    BACKGROUND_CHOICES = [
        ("cover", "На весь екран"),
        ("tile", "Плитка (2000-і)"),
        ("dim", "Затемнене фото"),
    ]


    font_family = models.CharField(
        "Шрифт",
        max_length=100,
        choices=[
            ("Arial", "Arial"),
            ("Verdana", "Verdana"),
            ("Times New Roman", "Times New Roman"),
            ("Courier New", "Courier New"),
            ("Georgia", "Georgia"),
            ("Tahoma", "Tahoma"),
            ("Roboto", "Roboto"),
            ("Open Sans", "Open Sans"),
            ("Lato", "Lato"),
            ("Montserrat", "Montserrat"),
            ("Monospace", "Monospace"),
        ],
        default="Arial",
    )

    custom_css = models.TextField("Кастомний CSS", blank=True)

    # системна чи кастомна
    is_system = models.BooleanField(default=False, verbose_name="Системна тема")
    is_active = models.BooleanField(default=False, verbose_name="Активна тема")

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="themes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    css_file = models.FileField(upload_to="themes/css/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name) or 'theme'
            self.slug = base
            i = 1
            while Theme.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base}-{i}"
                i += 1
        super().save(*args, **kwargs)


        # додаємо таймштамп щоб уникнути кешування
        filename = f"{self.slug or self.id}_{int(time.time())}.css"

        # видаляємо старий CSS якщо був
        if self.css_file:
            self.css_file.delete(save=False)

        # зберігаємо у FileField (MEDIA)

        super().save(update_fields=["css_file"])

    def __str__(self):
        return self.name
