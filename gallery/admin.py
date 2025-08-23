from django.contrib import admin
from .models import GalleryItem

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    actions = ['approve_items', 'reject_items']

    def approve_items(self, request, queryset):
        queryset.update(status='approved')
    approve_items.short_description = "Схвалити вибрані"

    def reject_items(self, request, queryset):
        queryset.update(status='rejected')
    reject_items.short_description = "Відхилити вибрані"
