from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Material(models.Model):
    name = models.CharField(max_length=50, verbose_name='Назва матеріалу')
    description = models.TextField(null=True,blank=True,verbose_name='Опис')
    file = models.FileField(upload_to='material/file',null=True,blank=True,verbose_name='Файл')
    image = models.ImageField(upload_to='material/image',null=True,blank=True,verbose_name='Фото')
    yt_url = models.CharField(max_length=250,null=True,blank=True,verbose_name='Посилання ют')
    creator = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='Автор')
    creat_time = models.DateTimeField(auto_now_add=True,verbose_name='Час створення')
    update_time = models.DateTimeField(auto_now_add=True,verbose_name='Час оновлення')
    
    def __str__(self):
        return self.name