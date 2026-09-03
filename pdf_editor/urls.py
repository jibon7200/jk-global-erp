from django.urls import path
from . import views

app_name = 'pdf_editor'

urlpatterns = [
    path('', views.project_list_view, name='project_list'),
    path('new/', views.project_create_view, name='project_create'),
    path('<int:pk>/edit/', views.project_edit_view, name='project_edit'),
    path('<int:pk>/add-files/', views.project_add_files_view, name='project_add_files'),
    path('<int:pk>/save-state/', views.project_save_state_view, name='project_save_state'),
    path('<int:pk>/export/', views.project_export_view, name='project_export'),
    path('thumbnail/<int:source_id>/<int:page_number>/', views.page_thumbnail_view, name='page_thumbnail'),
]