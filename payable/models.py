from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Supplier(models.Model):
    """
    A supplier/partner/vendor that JK GLOBAL owes money to —
    the OPPOSITE of the Due module (where customers owe us).
    """
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='suppliers_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_current_payable(self):
        total_owed = self.charges.aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
        total_paid = self.payments.aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
        return total_owed - total_paid

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Supplier"
        ordering = ['name']


class SupplierCharge(models.Model):
    """An amount we owe to a supplier — e.g. goods/services received on credit."""
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='charges')
    date = models.DateField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplier_charges_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.supplier.name} — Owed ৳{self.amount} on {self.date}"

    class Meta:
        ordering = ['-date', '-created_at']


class SupplierPayment(models.Model):
    """A payment WE made to a supplier, reducing what we owe them."""
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='payments')
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    note = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='supplier_payments_created')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.supplier.name} — Paid ৳{self.amount} on {self.date}"

    class Meta:
        ordering = ['-date', '-created_at']
