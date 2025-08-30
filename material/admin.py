from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Material

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'creater', 'creat_time', 'update_time')
    search_fields = ('creater')

admin.site.register(Material)