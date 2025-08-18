# from django.urls import path
# from .apps import CatalogConfig
# from .views import ProductListView, ProductDetailView
#
# app_name = CatalogConfig.name
#
# urlpatterns = [
#     path('', ProductListView.as_view(), name='product_list'),
#     path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
# ]

from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),           # /catalog/ → главная с баннером
    path('products/', views.ProductListView.as_view(), name='product_list'),  # /catalog/products/ → список товаров
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
]