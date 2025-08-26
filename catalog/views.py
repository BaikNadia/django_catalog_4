from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic import UpdateView, DeleteView, TemplateView
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm

class HomeView(TemplateView):
    template_name = 'catalog/home.html'

# Остальные представления...
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        # ✅ Правильно: все опубликованные товары
        return Product.objects.filter(publication_status='published')

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



class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Удалять может: владелец ИЛИ модератор
        if obj.owner != self.request.user and not self.request.user.has_perm('catalog.delete_product'):
            raise PermissionDenied("У вас нет прав на удаление этого товара.")
        return obj
