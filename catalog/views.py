from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic import UpdateView, DeleteView, TemplateView
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

class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        messages.success(self.request, f"Товар '{form.cleaned_data['name']}' успешно создан.")
        return super().form_valid(form)

# class ProductUpdateView(UpdateView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'catalog/product_form.html'
#     success_url = reverse_lazy('catalog:product_list')
#
#     def form_valid(self, form):
#         messages.success(self, f"Товар '{form.cleaned_data['name']}' успешно обновлён.")
#         return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Товар '{form.cleaned_data['name']}' успешно обновлён."
        )
        return response

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = self.get_object()
        messages.success(self.request, f"Товар '{product.name}' успешно удалён.")
        return super().form_valid(form)
