from django.urls import path
from . import views

app_name = 'dues'

urlpatterns = [
    path('', views.customer_list_view, name='customer_list'),
    path('add/', views.customer_add_view, name='customer_add'),
    path('report/', views.due_report_view, name='due_report'),
    path('<int:pk>/', views.customer_detail_view, name='customer_detail'),
    path('<int:pk>/charge/add/', views.charge_add_view, name='charge_add'),
    path('<int:pk>/payment/add/', views.payment_add_view, name='payment_add'),
]