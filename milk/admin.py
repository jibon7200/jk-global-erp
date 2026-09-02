from django.contrib import admin
from .models import MilkProduct, MilkPurchase, MilkSale


@admin.register(MilkProduct)
class MilkProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(MilkPurchase)
class MilkPurchaseAdmin(admin.ModelAdmin):
    list_display = ('product', 'date', 'quantity_bags', 'price_per_bag', 'total_amount', 'created_by')
    list_filter = ('product', 'date')
    search_fields = ('product__name',)
    readonly_fields = ('total_amount',)


@admin.register(MilkSale)
class MilkSaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'date', 'quantity_bags', 'price_per_bag', 'total_amount', 'created_by')
    list_filter = ('product', 'date')
    search_fields = ('product__name',)
    readonly_fields = ('total_amount',)