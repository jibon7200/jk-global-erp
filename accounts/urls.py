from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('users/', views.user_list_view, name='user_list'),
    path('users/add/', views.user_add_view, name='user_add'),
    path('users/<int:pk>/edit/', views.user_edit_view, name='user_edit'),
]