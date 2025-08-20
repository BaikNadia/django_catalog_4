from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
]


# from django.urls import path
# from . import views
#
# app_name = 'catalog'
#
# urlpatterns = [
#     path('', views.HomeView.as_view(), name='home'),           # /catalog/ → главная с баннером
#     path('products/', views.ProductListView.as_view(), name='product_list'),  # /catalog/products/ → список товаров
#     path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
# ]

