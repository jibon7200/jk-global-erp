from django.urls import path
from . import views

app_name = 'travel'

urlpatterns = [
    path('tickets/', views.ticket_list_view, name='ticket_list'),
    path('tickets/add/', views.ticket_add_view, name='ticket_add'),
    path('tickets/<int:pk>/edit/', views.ticket_edit_view, name='ticket_edit'),

    path('visa/', views.visa_list_view, name='visa_list'),
    path('visa/add/', views.visa_add_view, name='visa_add'),
    path('visa/<int:pk>/edit/', views.visa_edit_view, name='visa_edit'),

    path('passport/', views.passport_list_view, name='passport_list'),
    path('passport/add/', views.passport_add_view, name='passport_add'),
    path('passport/<int:pk>/edit/', views.passport_edit_view, name='passport_edit'),

    path('manpower/', views.manpower_list_view, name='manpower_list'),
    path('manpower/add/', views.manpower_add_view, name='manpower_add'),
    path('manpower/<int:pk>/edit/', views.manpower_edit_view, name='manpower_edit'),
]