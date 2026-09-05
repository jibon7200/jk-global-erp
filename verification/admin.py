from django.contrib import admin
from .models import VerificationConfig


@admin.register(VerificationConfig)
class VerificationConfigAdmin(admin.ModelAdmin):
    list_display = ('country_or_provider', 'service_type', 'method', 'is_active')
    list_filter = ('service_type', 'method', 'is_active')
    search_fields = ('country_or_provider',)