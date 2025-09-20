from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from themes.models import Theme


class Workshop(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField("Слаг", max_length=220, unique=True, blank=True)
    description = models.TextField("Опис", blank=True)
    start_at = models.DateTimeField("Початок", null=True, blank=True)
    location = models.CharField("Локація", max_length=200, blank=True)
    theme = models.ForeignKey(
        Theme,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workshops"
    )
    is_published = models.BooleanField("Опубліковано", default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_workshops"
    )
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        ordering = ["-start_at", "-created_at"]
        verbose_name = "Воркшоп"
        verbose_name_plural = "Воркшопи"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "workshop"
            self.slug = base
            i = 1
            while Workshop.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base}-{i}"
                i += 1
        super().save(*args, **kwargs)

    def publish(self):
        self.is_published = True
        self.save(update_fields=["is_published"])

    def get_absolute_url(self):
        return reverse("workshops:detail", kwargs={"slug": self.slug})


class GalleryItem(models.Model):
    MEDIA_CHOICES = (
        ("image", "Зображення"),
        ("video", "Відео"),
    )
    title = models.CharField("Заголовок", max_length=200)
    file = models.FileField("Файл", upload_to="gallery/")
    media_type = models.CharField("Тип", max_length=10, choices=MEDIA_CHOICES, default="image")
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="gallery_items")
    created_at = models.DateTimeField("Створено", auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Елемент галереї"
        verbose_name_plural = "Галерея"

    def __str__(self):
        return self.title
