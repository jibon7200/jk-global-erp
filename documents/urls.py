from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.document_list_view, name='document_list'),
    path('upload/', views.document_upload_view, name='document_upload'),
    path('<int:pk>/edit/', views.document_edit_view, name='document_edit'),
    path('<int:pk>/export/', views.document_export_view, name='document_export'),
    path('<int:pk>/upload-element/', views.element_image_upload_view, name='element_image_upload'),
    path('<int:pk>/ai-assist/', views.document_ai_assist_view, name='document_ai_assist'),
]