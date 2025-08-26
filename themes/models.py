# logika_portal/workshops/models.py
from django.db import models
from logika_portal.themes.models import Theme
from workshops.models import Workshop

class Workshop(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="workshops")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
