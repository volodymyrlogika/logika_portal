from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    speciality = (
        ("-", 'none'),
        ('+-', "soso"),
        ('+', "indeed"),
        ('++', "VERY NEED")
    )
    speciality = models.CharField(choices=speciality, default="-")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)