from django.contrib import admin
from .models import GalleryItem


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'uploader', 'status', 'created_at')
    list_filter = ('status', 'uploader')
    search_fields = ('title', 'caption', 'tags__name')
    actions = ['approve_items', 'reject_items']  # 🔹 додаємо екшени сюди

    @admin.action(description="Схвалити вибрані")
    def approve_items(self, request, queryset):
        queryset.update(status="approved")

    @admin.action(description="Відхилити вибрані")
    def reject_items(self, request, queryset):
        queryset.update(status="rejected")
