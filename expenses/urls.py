from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('', views.expense_list_view, name='expense_list'),
    path('add/', views.expense_add_view, name='expense_add'),
    path('<int:pk>/edit/', views.expense_edit_view, name='expense_edit'),
]