from django.db import models
from django.conf import settings


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
