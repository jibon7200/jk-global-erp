from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class AirTicket(models.Model):
    """
    Records every air ticket transaction.
    Profit is ALWAYS calculated automatically as:
        Profit = Customer Payment - My Payment/Cost
    Staff can enter this record, but the profit value itself is
    only ever displayed to Admin (enforced in the view/template,
    not just hidden by convention).
    """

    date = models.DateField()

    passport_holder_name = models.CharField(max_length=200)

    passport_number = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Used for fast searching across records."
    )

    number_of_tickets = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    customer_payment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Amount the customer paid us."
    )

    my_payment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Our actual cost/payment to the airline or vendor."
    )

    profit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False,
        help_text="Automatically calculated: customer_payment - my_payment."
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='air_tickets_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.profit = self.customer_payment - self.my_payment
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.passport_holder_name} — {self.number_of_tickets} ticket(s) on {self.date}"

    class Meta:
        verbose_name = "Air Ticket"
        verbose_name_plural = "Air Tickets"
        ordering = ['-date', '-created_at']
class Visa(models.Model):
    """
    Records every visa transaction.
    Profit = Customer Payment - My Visa Cost/Payment (calculated automatically).
    """

    date = models.DateField()
    passport_holder_name = models.CharField(max_length=200)
    passport_number = models.CharField(max_length=50, db_index=True)

    number_of_visa = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of Visa/Passport for this transaction."
    )

    customer_payment = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    my_payment = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Our actual visa cost/payment."
    )

    profit = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='visas_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.profit = self.customer_payment - self.my_payment
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.passport_holder_name} — Visa on {self.date}"

    class Meta:
        verbose_name = "Visa"
        verbose_name_plural = "Visas"
        ordering = ['-date', '-created_at']


class Passport(models.Model):
    """
    Records every passport transaction.
    Profit = Customer Payment - My Passport Cost/Payment (calculated automatically).
    """

    date = models.DateField()
    passport_holder_name = models.CharField(max_length=200)
    passport_number = models.CharField(max_length=50, db_index=True)

    number_of_passports = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    customer_payment = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    my_payment = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Our actual passport cost/payment."
    )

    profit = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='passports_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.profit = self.customer_payment - self.my_payment
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.passport_holder_name} — Passport on {self.date}"

    class Meta:
        verbose_name = "Passport"
        verbose_name_plural = "Passports"
        ordering = ['-date', '-created_at']


class Manpower(models.Model):
    """
    Records every manpower transaction.
    Profit = Customer Payment - My Manpower Cost/Payment (calculated automatically).
    """

    date = models.DateField()
    passport_holder_name = models.CharField(max_length=200)
    passport_number = models.CharField(max_length=50, db_index=True)

    number_of_manpower = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    customer_payment = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    my_payment = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Our actual manpower cost/payment."
    )

    profit = models.DecimalField(max_digits=12, decimal_places=2, editable=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='manpower_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.profit = self.customer_payment - self.my_payment
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.passport_holder_name} — Manpower on {self.date}"

    class Meta:
        verbose_name = "Manpower"
        verbose_name_plural = "Manpower Records"
        ordering = ['-date', '-created_at']