from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published', 'views_count')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'views_count')  # Поля только для чтения
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'preview')
        }),
        ('Публикация', {
            'fields': ('is_published',)
        }),
        ('Мета-информация', {
            'fields': ('created_at', 'views_count'),
            'classes': ('collapse',),  # Сворачиваемая секция
        }),
    )
