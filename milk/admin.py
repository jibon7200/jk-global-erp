from django.contrib import admin
from .models import MilkProduct


@admin.register(MilkProduct)
class MilkProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
