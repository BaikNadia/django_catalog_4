from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    # Поле email делаем уникальным и обязательным
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким email уже существует.'
        }
    )

    # Аватар
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        default='avatars/default.jpg'
    )

    # Номер телефона с валидацией
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+79991234567'. Допускается до 15 цифр."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True
    )

    # Страна
    country = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    # Делаем email полем для входа
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username остаётся обязательным при создании через createsuperuser

    def __str__(self):
        return self.email
