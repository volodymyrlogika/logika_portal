from django.contrib import admin
from .models import GalleryItem

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'uploader', 'theme', 'created_at', 'approved')
    list_filter = ('approved', 'media_type', 'theme', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('approved',)  # ✅ можна змінювати статус прямо зі списку
    actions = ['approve_items', 'reject_items']

    @admin.action(description="Схвалити вибрані")
    def approve_items(self, request, queryset):
        queryset.update(approved=True)

    @admin.action(description="Відхилити вибрані")
    def reject_items(self, request, queryset):
        queryset.update(approved=False)
