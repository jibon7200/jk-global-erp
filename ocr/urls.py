from django.urls import path
from . import views

app_name = 'ocr'

urlpatterns = [
    path('passport-scan/', views.scan_upload_view, name='scan_upload'),
    path('passport-scan/<int:pk>/review/', views.scan_review_view, name='scan_review'),
    path('passport-scan/history/', views.scan_list_view, name='scan_list'),
]