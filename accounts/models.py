from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    JK Global Custom User Model.
    Extends Django's built-in User to add a 'role' field.
    This role decides what a user can see and do:
    - ADMIN  -> Full access, including Profit (only Jibon initially)
    - STAFF  -> Normal business entries, NO access to Profit
    """

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STAFF = 'STAFF', 'Staff'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STAFF,
        help_text="Admin has full access including Profit. Staff cannot see Profit."
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Optional contact number for this user."
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_admin_role(self):
        """Helper method: returns True if this user is an Admin."""
        return self.role == self.Role.ADMIN

    def is_staff_role(self):
        """Helper method: returns True if this user is Staff."""
        return self.role == self.Role.STAFF

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['username']