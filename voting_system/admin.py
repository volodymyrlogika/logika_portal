from django.contrib import admin
from .models import Voting, Option, Vote

from unfold.admin import ModelAdmin

class OptionInline(admin.TabularInline): # TabularInline для компактного вигляду
    model = Option
    extra = 3  # Кількість порожніх форм для додавання нових коментарів

@admin.register(Voting)
class VotingAdmin(ModelAdmin):
    list_display = ('name', 'author', 'data_start', 'data_end', 'created_at')
    search_fields = ('name', 'author__username', )
    list_filter = ('author', 'data_start', 'data_end')
    
    fieldsets = (
        ('Головна інформація', {
            'fields': ('name', 'author')
        }),
        ('Дати', {
            'fields': ('data_start', 'data_end', )
        }),
    )
    
    inlines = [OptionInline]


admin.site.register(Option) 
admin.site.register(Vote)
