from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Expense(models.Model):
    """
    Records office and other business expenses.
    These are included in the overall accounting/profit calculation
    later on the Profit page (as a deduction from total profit).
    """

    class Category(models.TextChoices):
        OFFICE_RENT = 'OFFICE_RENT', 'Office Rent'
        EMPLOYEE_SALARY = 'EMPLOYEE_SALARY', 'Employee Salary'
        ELECTRICITY_BILL = 'ELECTRICITY_BILL', 'Electricity Bill'
        INTERNET_BILL = 'INTERNET_BILL', 'Internet Bill'
        TRANSPORTATION = 'TRANSPORTATION', 'Transportation'
        OFFICE_EXPENSES = 'OFFICE_EXPENSES', 'Office Expenses'
        OTHER_EXPENSES = 'OTHER_EXPENSES', 'Other Expenses'

    date = models.DateField()

    category = models.CharField(
        max_length=30,
        choices=Category.choices
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    note = models.CharField(
        max_length=255,
        blank=True,
        help_text="Short note/description, e.g. 'August Office Rent'."
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expenses_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_category_display()} — ৳{self.amount} on {self.date}"

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ['-date', '-created_at']