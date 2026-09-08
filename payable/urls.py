from django.urls import path
from . import views

app_name = 'payable'

urlpatterns = [
    path('', views.supplier_list_view, name='supplier_list'),
    path('add/', views.supplier_add_view, name='supplier_add'),
    path('report/', views.payable_report_view, name='payable_report'),
    path('<int:pk>/', views.supplier_detail_view, name='supplier_detail'),
    path('<int:pk>/charge/add/', views.charge_add_view, name='charge_add'),
    path('<int:pk>/payment/add/', views.payment_add_view, name='payment_add'),
]