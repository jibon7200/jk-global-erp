from django.db import models
from django.conf import settings


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

    theme_primary_color = models.CharField(max_length=7, default="#1e3a5f", help_text="Sidebar and primary buttons.")
    theme_accent_color = models.CharField(max_length=7, default="#3b82f6", help_text="Highlights, active menu, links.")
    theme_text_color = models.CharField(max_length=7, default="#0f172a", help_text="Main body text color.")
    theme_background_color = models.CharField(max_length=7, default="#f1f5f9", help_text="Page background color.")

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


class AIImageUsage(models.Model):
    """
    Tracks how many AI image generations each user has made TODAY,
    so we can enforce a small daily limit — AI image generation is
    NOT truly unlimited/free even on Google's free tier, so this
    protects against accidentally exceeding it.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ai_image_usage'
    )

    date = models.DateField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')
        verbose_name = "AI Image Usage"
        verbose_name_plural = "AI Image Usage Records"

    def __str__(self):
        return f"{self.user.username} — {self.date} — {self.count} image(s)"       