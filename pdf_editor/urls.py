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
    path('<int:pk>/upload-element/', views.page_element_image_upload_view, name='page_element_image_upload'),
    path('<int:pk>/ai-assist/', views.pdf_ai_assist_view, name='pdf_ai_assist'),
    path('<int:pk>/page/<str:page_id>/edit/', views.page_editor_view, name='page_editor'),
    path('thumbnail/<int:source_id>/<int:page_number>/', views.page_thumbnail_view, name='page_thumbnail'),
    path('<int:pk>/convert-to-word/', views.project_convert_to_word_view, name='project_convert_to_word'),
    path('<int:pk>/upload-word/', views.project_upload_word_view, name='project_upload_word'),
    path('<int:pk>/delete/', views.project_delete_view, name='project_delete'),
]