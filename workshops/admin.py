from django.contrib import admin
from .models import Workshop



@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'theme', 'start_at', 'location', 'is_published')
    list_filter = ('is_published', 'theme')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
