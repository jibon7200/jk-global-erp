from django.urls import path
from . import views

app_name = 'milk'

urlpatterns = [
    path('products/', views.product_list_view, name='product_list'),
    path('products/add/', views.product_add_view, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit_view, name='product_edit'),
]