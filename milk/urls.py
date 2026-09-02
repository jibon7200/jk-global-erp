from django.urls import path
from . import views

app_name = 'milk'

urlpatterns = [
    path('products/', views.product_list_view, name='product_list'),
    path('products/add/', views.product_add_view, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit_view, name='product_edit'),

    path('purchases/', views.purchase_list_view, name='purchase_list'),
    path('purchases/add/', views.purchase_add_view, name='purchase_add'),

    path('sales/', views.sale_list_view, name='sale_list'),
    path('sales/add/', views.sale_add_view, name='sale_add'),

    path('stock/', views.stock_view, name='stock'),
]