from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profit/', views.profit_view, name='profit'),
    path('settings/', views.settings_view, name='settings'),
    path('theme/', views.theme_view, name='theme'),
]