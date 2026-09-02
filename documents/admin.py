from django.contrib import admin
from .models import DocumentEdit


@admin.register(DocumentEdit)
class DocumentEditAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'created_at')
