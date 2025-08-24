from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Theme(models.Model):
    name = models.CharField('Назва', max_length=120, unique=True)
    slug = models.SlugField('Слаг', max_length=140, unique=True, blank=True)
    description = models.TextField('Опис', blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_themes', verbose_name='Створив'
    )
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Тема'
        verbose_name_plural = 'Теми'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Workshop(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('Слаг', max_length=220, unique=True, blank=True)
    description = models.TextField('Опис', blank=True)
    start_at = models.DateTimeField('Початок', null=True, blank=True)
    end_at = models.DateTimeField('Кінець', null=True, blank=True)
    location = models.CharField('Локація', max_length=200, blank=True)
    capacity = models.PositiveIntegerField('Кількість місць', null=True, blank=True)
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True, related_name='workshops', verbose_name='Тема')
    is_published = models.BooleanField('Опубліковано', default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_workshops', verbose_name='Створив'
    )
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        ordering = ['-start_at', '-created_at']
        verbose_name = 'Воркшоп'
        verbose_name_plural = 'Воркшопи'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or 'workshop'
            self.slug = base
            i = 1
            while Workshop.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base}-{i}"
                i += 1
        super().save(*args, **kwargs)


def gallery_upload_path(instance, filename):
    return f"gallery/{instance.uploader_id or 'anon'}/{filename}"

class GalleryItem(models.Model):
    MEDIA_CHOICES = (
        ('image', 'Зображення'),
        ('video', 'Відео'),
        ('file', 'Файл'),
    )
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Опис', blank=True)
    file = models.FileField('Файл', upload_to=gallery_upload_path)
    media_type = models.CharField('Тип медіа', max_length=10, choices=MEDIA_CHOICES, default='image')
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_uploads', verbose_name='Завантажив')
    workshop = models.ForeignKey(Workshop, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_items', verbose_name='Воркшоп')
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_items', verbose_name='Тема')
    approved = models.BooleanField('Схвалено модератором', default=False)
    created_at = models.DateTimeField('Створено', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Елемент галереї'
        verbose_name_plural = 'Галерея'

    def __str__(self):
        return self.title
