from django.contrib import admin
from .models import GalleryItem


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "uploaded_by", "status", "created_at")
    list_filter = ("status", "uploaded_by")
    search_fields = ("title", "uploaded_by__username")
    list_editable = ("status",)

    @admin.action(description="Схвалити вибрані")
    def approve_items(self, request, queryset):
        queryset.update(status="approved")

    @admin.action(description="Відхилити вибрані")
    def reject_items(self, request, queryset):
        queryset.update(status="rejected")
