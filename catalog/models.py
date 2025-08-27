from django.db import models
from users.models import User


PUBLICATION_STATUS_CHOICES = [
    ('draft', 'Черновик'),
    ('published', 'Опубликован'),
    ('archived', 'Архив'),
]


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="наименование")
    description = models.TextField(blank=True, null=True, verbose_name="описание")

    objects = models.Manager()

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="наименование")
    description = models.TextField(blank=True, null=True, verbose_name="описание")
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name="изображение"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        blank=True,
        verbose_name="категория"
    )
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="дата последнего изменения")

    # Используем глобальную константу
    publication_status = models.CharField(
        max_length=20,
        verbose_name="статус публикации",
        choices=PUBLICATION_STATUS_CHOICES,
        default='draft'
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="владелец"
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ['-created_at']
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию товара"),
        ]

    def __str__(self):
        return self.name
