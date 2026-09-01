from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class MilkProduct(models.Model):
    """
    Represents a 25 KG Milk Powder product (e.g. DANO Full Cream,
    New Zealand Full Cream, Amul Indian, etc).

    Admin can add new products anytime from the app itself —
    no code change needed when a new brand/product is introduced.
    """

    name = models.CharField(
        max_length=150,
        unique=True,
        help_text="e.g. DANO Full Cream, New Zealand Full Cream"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Inactive products are hidden from purchase/sale forms but kept for history."
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='milk_products_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Milk Product"
        verbose_name_plural = "Milk Products"
        ordering = ['name']

class MilkPurchase(models.Model):
    """
    Records every time Jibon purchases milk powder bags from a supplier.
    Saving this record automatically increases the stock of the
    related product (handled in the view using a database transaction
    to keep stock calculations safe and consistent).
    """

    product = models.ForeignKey(
        MilkProduct,
        on_delete=models.PROTECT,
        related_name='purchases',
        help_text="Which product was purchased."
    )

    date = models.DateField()

    quantity_bags = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of 25 KG bags purchased."
    )

    price_per_bag = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Purchase price per bag in BDT."
    )

    total_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        editable=False,
        help_text="Automatically calculated: quantity_bags x price_per_bag."
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='milk_purchases_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Always recalculate total_amount from quantity and price,
        # so it can never be entered incorrectly by mistake.
        self.total_amount = Decimal(self.quantity_bags) * self.price_per_bag
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} — {self.quantity_bags} bags on {self.date}"

    class Meta:
        verbose_name = "Milk Purchase"
        verbose_name_plural = "Milk Purchases"
        ordering = ['-date', '-created_at']        
