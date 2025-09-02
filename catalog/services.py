from django.core.cache import cache
from config.settings import CACHE_ENABLED
from catalog.models import Product


def get_products_from_cache():
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "product_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products


# from .models import Product
#
#
# def get_products_by_category(category_id):
#     """
#     Возвращает список продуктов в указанной категории.
#     Если категория не существует, возвращает пустой QuerySet.
#     """
#     return Product.objects.filter(
#         category_id=category_id,
#         publication_status='published'
#     ).select_related('category', 'owner')
