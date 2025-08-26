from django.contrib import admin
from logika_portal.themes.models import Theme
from .models import Workshop

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name',)

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'theme', 'start_at', 'location', 'is_published')
    list_filter = ('is_published', 'theme')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
