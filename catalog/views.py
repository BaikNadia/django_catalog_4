# from django.views.generic import ListView, DetailView
# from .models import Product
#
# class ProductListView(ListView):
#     model = Product
#
#
# class ProductDetailView(DetailView):
#     model = Product

from django.views.generic import ListView, DetailView, TemplateView
from .models import Product

# Главная страница с баннером
class HomeView(TemplateView):
    template_name = 'catalog/home.html'

# Список товаров (перенесён на отдельный URL)
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'  # убедимся, что используется правильный шаблон
    context_object_name = 'products'

# Детали товара
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
