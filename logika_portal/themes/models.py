from django.db import models

class Theme(models.Model):
    name = models.CharField(max_length=100)
    background_color = models.CharField(max_length=20, default='#ffffff')
    text_color = models.CharField(max_length=20, default='#000000')
    custom_css = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
