from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
import os
def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"  # унікальне ім'я
    return os.path.join('avatars', f'user_{instance.user.id}', filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(
        max_length=20,
        choices=[("light", "Світла"), ("dark", "Темна")],
        default="light"
    )
    bio = models.TextField(blank=True, null=True, verbose_name="Біо")  # ✅ додано
    avatar = models.ImageField(  # ✅ додано
        upload_to=user_avatar_path,
        blank=True,
        null=True,
        verbose_name="Аватар"
    )
    custom_theme = models.ForeignKey(
        "themes.Theme",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profiles"
    )

    def __str__(self):
        return f"{self.user.username} Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "profile"):
        instance.profile.save()