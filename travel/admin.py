from django.contrib import admin
from .models import AirTicket, Visa, Passport, Manpower


@admin.register(AirTicket)
class AirTicketAdmin(admin.ModelAdmin):
    list_display = (
        'passport_holder_name', 'passport_number', 'date',
        'number_of_tickets', 'customer_payment', 'my_payment',
        'profit', 'created_by'
    )
    list_filter = ('date',)
    search_fields = ('passport_holder_name', 'passport_number')
    readonly_fields = ('profit',)


@admin.register(Visa)
class VisaAdmin(admin.ModelAdmin):
    list_display = (
        'passport_holder_name', 'passport_number', 'date',
        'number_of_visa', 'customer_payment', 'my_payment',
        'profit', 'created_by'
    )
    list_filter = ('date',)
    search_fields = ('passport_holder_name', 'passport_number')
    readonly_fields = ('profit',)


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    list_display = (
        'passport_holder_name', 'passport_number', 'date',
        'number_of_passports', 'customer_payment', 'my_payment',
        'profit', 'created_by'
    )
    list_filter = ('date',)
    search_fields = ('passport_holder_name', 'passport_number')
    readonly_fields = ('profit',)


@admin.register(Manpower)
class ManpowerAdmin(admin.ModelAdmin):
    list_display = (
        'passport_holder_name', 'passport_number', 'date',
        'number_of_manpower', 'customer_payment', 'my_payment',
        'profit', 'created_by'
    )
    list_filter = ('date',)
    search_fields = ('passport_holder_name', 'passport_number')
    readonly_fields = ('profit',)
