from django.contrib import admin
from .models import Supplier, SupplierCharge, SupplierPayment

admin.site.register(Supplier)
admin.site.register(SupplierCharge)
admin.site.register(SupplierPayment)
