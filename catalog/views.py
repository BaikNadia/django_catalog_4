from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic import UpdateView, DeleteView, TemplateView
from django.core.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404
from django.core.cache import cache

from django.urls import reverse_lazy
from .models import Product, Category
from .forms import ProductForm



class HomeView(TemplateView):
    template_name = 'catalog/home.html'

class ProductByCategoryView(ListView):
    """
    Представление для отображения всех продуктов в указанной категории.
    """
    model = Product
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products'
    paginate_by = 6  # Опционально: пагинация

    def get_queryset(self):
        # Получаем категорию по ID из URL
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        # Фильтруем только опубликованные товары
        return Product.objects.filter(
            category=self.category,
            publication_status='published'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        # Ключ кэша
        cache_key = 'published_products'
        # Время жизни кэша — 15 минут
        cache_timeout = 60 * 15

        # Попытка получить из кэша
        products = cache.get(cache_key)
        if products is None:
            # Если нет в кэше — получаем из БД и сохраняем
            products = Product.objects.filter(publication_status='published')
            cache.set(cache_key, products, cache_timeout)

        return products

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ProductUnpublishView(PermissionRequiredMixin, UpdateView):
    model = Product
    fields = []  # не редактируем, только действие
    template_name = 'catalog/product_confirm_unpublish.html'
    success_url = reverse_lazy('catalog:product_list')
    permission_required = 'catalog.can_unpublish_product'

    def form_valid(self, form):
        product = form.instance
        product.is_published = False
        product.save()
        return super().form_valid(form)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        # Очистка кэша после создания
        cache.delete('published_products')
        return super().form_valid(form)



class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise PermissionDenied("Вы не можете редактировать этот товар.")
        return obj

    def form_valid(self, form):
        # Очистка кэша после редактирования
        cache.delete('published_products')
        return super().form_valid(form)



class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user and not self.request.user.has_perm('catalog.delete_product'):
            raise PermissionDenied("У вас нет прав на удаление этого товара.")
        return obj

    def delete(self, *args, **kwargs):
        # Очистка кэша после удаления
        cache.delete('published_products')
        return super().delete(*args, **kwargs)
