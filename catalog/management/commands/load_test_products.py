from django.core.management.base import BaseCommand
from django.db import transaction
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Удаляет все данные и загружает тестовые продукты'

    @transaction.atomic
    def handle(self, *args, **options):
        # Удаляем все продукты и категории
        self.stdout.write('Удаляем существующие данные...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('✅ Все данные удалены'))

        # Создаём категории
        category_laptops = Category.objects.create(
            name='Ноутбуки',
            description='Портативные компьютеры для работы и игр'
        )
        category_phones = Category.objects.create(
            name='Смартфоны',
            description='Современные мобильные телефоны'
        )
        self.stdout.write(self.style.SUCCESS('✅ Категории созданы'))

        # Создаём продукты
        products = [
            Product(
                name='MacBook Pro 14',
                description='Мощный ноутбук на чипе M3, 16 ГБ ОЗУ, 512 ГБ SSD',
                category=category_laptops,
                purchase_price=159990.00
            ),
            Product(
                name='Dell XPS 13',
                description='Ультрабук с дисплеем 4K, 16 ГБ ОЗУ, 1 ТБ SSD',
                category=category_laptops,
                purchase_price=120000.00
            ),
            Product(
                name='iPhone 15',
                description='Смартфон с камерой 48 Мп, 6 ГБ ОЗУ, 128 ГБ',
                category=category_phones,
                purchase_price=79990.00
            ),
            Product(
                name='Samsung Galaxy S23',
                description='Флагманский смартфон с мощным процессором',
                category=category_phones,
                purchase_price=65000.00
            ),
        ]

        Product.objects.bulk_create(products)
        self.stdout.write(
            self.style.SUCCESS(f'✅ Успешно добавлено {len(products)} тестовых продуктов')
        )

        # Выводим итог
        self.stdout.write(self.style.NOTICE('📋 Добавленные продукты:'))
        for product in products:
            self.stdout.write(f" • {product.name} — {product.purchase_price} ₽")
