from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'description')
    ordering = ['name']
    list_per_page = 20

    # Опционально: поля при редактировании
    fields = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'purchase_price',
        'created_at',
        'updated_at'
    )
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('name', 'category__name')
    ordering = ['-created_at']
    list_per_page = 20

    # Группировка полей при редактировании
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'image')
        }),
        ('Категория и цена', {
            'fields': ('category', 'purchase_price')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Сворачиваемая секция
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('category',)  # Удобно при большом числе категорий
