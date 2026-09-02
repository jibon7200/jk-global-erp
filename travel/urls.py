from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('tickets/', views.ticket_list_view, name='ticket_list'),
    path('tickets/add/', views.ticket_add_view, name='ticket_add'),
    path('tickets/<int:pk>/edit/', views.ticket_edit_view, name='ticket_edit'),
]