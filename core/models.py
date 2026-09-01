from django.db import models


class SiteSettings(models.Model):
    """
    Stores company-wide settings like the logo and company name.
    This is designed as a SINGLETON — meaning only ONE row of this
    table should ever exist. Admin can update the logo anytime from
    the Django Admin Panel without touching any code.
    """

    company_name = models.CharField(
        max_length=200,
        default="J.K. GLOBAL PRIVATE LIMITED"
    )

    managing_director_name = models.CharField(
        max_length=200,
        default="Jibon"
    )

    logo = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True,
        help_text="Upload the company logo. Recommended: PNG with transparent background, square or wide shape."
    )

    currency_symbol = models.CharField(
        max_length=5,
        default="৳"
    )

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Enforces the singleton pattern: no matter how many times
        someone tries to create a new SiteSettings row, it always
        overwrites row with id=1 instead of creating a second row.
        """
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Prevents accidental deletion of the one settings row."""
        pass

    @classmethod
    def get_settings(cls):
        """
        Safely fetches the single SiteSettings row.
        If it doesn't exist yet, creates it with defaults.
        Use this everywhere instead of SiteSettings.objects.get(...).
        """
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"