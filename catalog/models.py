from django.db import models



class Category(models.Model):
    """
    Модель категории товаров.
    """
    name = models.CharField(
        max_length=150,
        verbose_name="наименование"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="описание"
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель продукта.
    """
    name = models.CharField(
        max_length=200,
        verbose_name="наименование"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="описание"
    )
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
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="цена за покупку"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="дата последнего изменения"
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
