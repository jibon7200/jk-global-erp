from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'date', 'amount', 'note', 'created_by')
    list_filter = ('category', 'date')
    search_fields = ('note',)
