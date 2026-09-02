from django.contrib import admin
from .models import Customer, DueCharge, DuePayment


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'created_by', 'created_at')
    search_fields = ('name', 'phone_number')


@admin.register(DueCharge)
class DueChargeAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date', 'description', 'amount', 'created_by')
    list_filter = ('date',)
    search_fields = ('customer__name',)


@admin.register(DuePayment)
class DuePaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date', 'amount', 'note', 'created_by')
    list_filter = ('date',)
    search_fields = ('customer__name',)
