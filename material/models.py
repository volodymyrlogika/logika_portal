from django.db import models

# Create your models here.

class Material(models.Model):
    advert_id = models.IntegerField()
    name = models.CharField(max_length=50)
    fille = models.FileField()
    image = models.ImageField()
    yt_url = models.CharField(max_length=80)
    creater = models.CharField(max_length=30)
    creat_time = models.DateTimeField(auto_now_add=True)
    Update_time = models.DateTimeField(auto_now_add=True)