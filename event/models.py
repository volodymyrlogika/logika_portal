from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
    speciality = (
        ("-", 'none'),
        ('+-', "soso"),
        ('+', "indeed"),
        ('++', "VERY NEED")
    )
    speciality = models.CharField(choices=speciality, default="-")
    user = models.ForeignKey(User, on_delete=models.CASCADE)    