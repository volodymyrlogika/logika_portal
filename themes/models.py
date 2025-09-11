import time
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User


class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    background_color = models.CharField("Колір фону", max_length=7, default="#ffffff")
    text_color = models.CharField("Колір тексту", max_length=7, default="#000000")

    background_image = models.ImageField(
        "Фонове зображення", upload_to="themes/backgrounds/", blank=True, null=True
    )

    BACKGROUND_CHOICES = [
        ("cover", "На весь екран"),
        ("tile", "Плитка (2000-і)"),
        ("dim", "Затемнене фото"),
    ]
    background_mode = models.CharField(
        max_length=20, choices=BACKGROUND_CHOICES, default="cover"
    )

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
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)  # спочатку зберігаємо, щоб був ID

        # 🔥 формуємо CSS в залежності від режиму фону
        bg_image_css = ""
        if self.background_image:
            if self.background_mode == "cover":
                bg_image_css = f"""
                body {{
                    background: url('{settings.MEDIA_URL}{self.background_image.name}') 
                                center/cover no-repeat fixed;
                }}
                """
            elif self.background_mode == "tile":
                bg_image_css = f"""
                body {{
                    background: url('{settings.MEDIA_URL}{self.background_image.name}') repeat;
                }}
                """
            elif self.background_mode == "dim":
                bg_image_css = f"""
                body::before {{
                    content: "";
                    position: fixed;
                    inset: 0;
                    background: url('{settings.MEDIA_URL}{self.background_image.name}') 
                                center/cover no-repeat;
                    filter: brightness(0.5);
                    z-index: -1;
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

        # додаємо таймштамп щоб уникнути кешування
        filename = f"{self.slug or self.id}_{int(time.time())}.css"

        # видаляємо старий CSS якщо був
        if self.css_file:
            self.css_file.delete(save=False)

        # зберігаємо у FileField (MEDIA)
        self.css_file.save(filename, ContentFile(css_content.strip()), save=False)
        super().save(update_fields=["css_file"])

    def __str__(self):
        return self.name
