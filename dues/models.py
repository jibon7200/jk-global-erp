from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Customer(models.Model):
    """
    A customer who owes (or has owed) money to JK GLOBAL.
    This customer ledger works across ALL businesses — Milk, Ticket,
    Visa, Passport, Manpower, or anything else — it is not tied to
    any specific Sale/Ticket record.
    """

    name = models.CharField(max_length=200)

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        help_text="Optional contact number."
    )

    notes = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional note about this customer."
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customers_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_current_due(self):
        """
        Calculates the current outstanding due LIVE from the database:
            Current Due = (Total Charges) - (Total Payments)
        Same live-calculation pattern used for Milk Stock — never
        stored separately, so it can never become inconsistent.
        """
        total_charged = self.charges.aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')

        total_paid = self.payments.aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')

        return total_charged - total_paid

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['name']


class DueCharge(models.Model):
    """
    Records an amount owed BY a customer TO us — e.g. goods or
    services given on credit ("বাকিতে দেওয়া হলো").
    """

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='charges'
    )

    date = models.DateField()

    description = models.CharField(
        max_length=255,
        help_text="e.g. '5 bags milk powder on credit', 'Air ticket booking'"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='due_charges_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} — Charge ৳{self.amount} on {self.date}"

    class Meta:
        verbose_name = "Due Charge"
        verbose_name_plural = "Due Charges"
        ordering = ['-date', '-created_at']


class DuePayment(models.Model):
    """
    Records a payment RECEIVED from a customer, reducing their due.
    """

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    date = models.DateField()

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    note = models.CharField(max_length=255, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='due_payments_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} — Paid ৳{self.amount} on {self.date}"

    class Meta:
        verbose_name = "Due Payment"
        verbose_name_plural = "Due Payments"
        ordering = ['-date', '-created_at']
