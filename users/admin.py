from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Опционально: настройка отображения в списке
class CustomUserAdmin(UserAdmin):
    # Поля, отображаемые в списке пользователей
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')

    # Фильтры в боковой панели
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # Поля, по которым можно искать
    search_fields = ('email', 'username', 'first_name', 'last_name')

    # Поля, редактируемые при клике на пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация',
         {'fields': ('username', 'first_name', 'last_name', 'phone_number', 'country', 'avatar')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Поля при создании нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    # Сортировка
    ordering = ('email',)


# Регистрируем модель с кастомным интерфейсом
admin.site.register(User, CustomUserAdmin)
