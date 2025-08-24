from django.contrib import admin
from .models import Theme, Workshop, GalleryItem

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

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'uploader', 'approved', 'created_at')
    list_filter = ('approved', 'media_type', 'theme')
    search_fields = ('title', 'description')
    actions = ['approve_selected']

    @admin.action(description='Схвалити вибрані')
    def approve_selected(self, request, queryset):
        queryset.update(approved=True)
