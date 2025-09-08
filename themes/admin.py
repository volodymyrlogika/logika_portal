from django.contrib import admin
from .models import Theme


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_by", "created_at")
    list_filter = ("is_active", "font_family")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}  # автозаповнення slug
    
