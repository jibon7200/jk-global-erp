from django.urls import path
from . import views

app_name = 'verification'

urlpatterns = [
    path('', views.status_home_view, name='status_home'),
    path('visa/', views.visa_check_view, name='visa_check'),
    path('passport/', views.passport_check_view, name='passport_check'),
    path('air-ticket/', views.air_ticket_check_view, name='air_ticket_check'),
    path('manpower/', views.manpower_check_view, name='manpower_check'),
]