import time
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User


# ==============================
# ТЕМИ
# ==============================
class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    background_color = models.CharField("Колір фону", max_length=7, default="#ffffff")
    text_color = models.CharField("Колір тексту", max_length=7, default="#000000")
    background_image = models.ImageField(
        "Фонове зображення", upload_to="themes/backgrounds/", blank=True, null=True
    )
    font_family = models.CharField(
        "Шрифт",
        max_length=100,
        choices=[("Arial", "Arial"), ("Verdana", "Verdana"), ("Times New Roman", "Times New Roman"),
                 ("Courier New", "Courier New"), ("Georgia", "Georgia"), ("Tahoma", "Tahoma"),
                 ("Roboto", "Roboto"), ("Open Sans", "Open Sans"), ("Lato", "Lato"),
                 ("Montserrat", "Montserrat"), ("Monospace", "Monospace")],
        default="Arial",
    )
    custom_css = models.TextField("Кастомний CSS", blank=True)

    is_active = models.BooleanField(default=False, verbose_name="Активна тема")
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="themes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # потрібен ID
        from .utils import create_theme_css
        create_theme_css(self)  # генеруємо css у static/css/themes

    def __str__(self):
        return self.name
        # Генеруємо CSS
        bg_image_css = ""
        if self.background_image:
            bg_image_css = f"""
            body {{
                background-image: url('{settings.MEDIA_URL}{self.background_image.name}');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            """

        css_content = f"""
        /* Автоматично створений CSS для теми: {self.name} */
        body {{
            background-color: {self.background_color};
            color: {self.text_color};
            font-family: '{self.font_family}', sans-serif;
        }}
        .navbar {{
            background-color: {self.background_color};
        }}
        a {{
            color: {self.text_color};
        }}
        {bg_image_css}
        {self.custom_css}
        """

        # додаємо таймштамп щоб уникнути кешу
        filename = f"{self.slug or self.id}_{int(time.time())}.css"

        # видаляємо старий CSS якщо був
        if self.css_file:
            self.css_file.delete(save=False)

        # зберігаємо у FileField (MEDIA)
        self.css_file.save(filename, ContentFile(css_content.strip()), save=False)
        super().save(update_fields=["css_file"])

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
        return self.title


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
