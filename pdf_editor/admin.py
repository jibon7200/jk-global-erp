from django.contrib import admin
from .models import PDFProject, PDFSourceFile


@admin.register(PDFProject)
class PDFProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'created_at')


@admin.register(PDFSourceFile)
class PDFSourceFileAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'project', 'created_at')