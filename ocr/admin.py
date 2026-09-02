from django.contrib import admin
from .models import PassportScan


@admin.register(PassportScan)
class PassportScanAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'passport_number', 'extraction_successful', 'reviewed_and_confirmed', 'created_by', 'created_at')
    list_filter = ('extraction_successful', 'reviewed_and_confirmed')
    search_fields = ('full_name', 'passport_number')
