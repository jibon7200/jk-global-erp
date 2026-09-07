from django.db import models
from django.conf import settings


class VerificationConfig(models.Model):
    """
    Data-driven configuration for status checking — this is what
    lets Admin add support for a new country/airline WITHOUT any
    code changes (per project spec section 31).

    For each country/provider + service type, this defines:
    - which fields the user must fill in
    - whether an official API exists, or only a website exists
    - the official website URL to fall back to
    """

    class ServiceType(models.TextChoices):
        VISA = 'VISA', 'Visa'
        PASSPORT = 'PASSPORT', 'Passport'
        AIR_TICKET = 'AIR_TICKET', 'Air Ticket'

    class Method(models.TextChoices):
        API = 'API', 'Official API (not yet integrated)'
        WEBSITE = 'WEBSITE', 'Official Website Only'
        MANUAL = 'MANUAL', 'Manual Verification Required'

    country_or_provider = models.CharField(
        max_length=150,
        help_text="Country name (for Visa/Passport) or Airline/Provider name (for Air Ticket)."
    )

    service_type = models.CharField(max_length=20, choices=ServiceType.choices)

    required_fields = models.JSONField(
        default=list,
        help_text='List of fields this country/provider needs, e.g. '
                   '[{"name": "passport_number", "label": "Passport Number"}, '
                   '{"name": "date_of_birth", "label": "Date of Birth"}]'
    )

    method = models.CharField(max_length=10, choices=Method.choices, default=Method.MANUAL)

    official_url = models.URLField(
        blank=True,
        help_text="Official government/airline verification website, if one exists."
    )

    instructions = models.TextField(
        blank=True,
        help_text="Any special notes for staff about verifying this country/provider."
    )

    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verification_configs_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.country_or_provider} — {self.get_service_type_display()}"

    class Meta:
        verbose_name = "Verification Configuration"
        verbose_name_plural = "Verification Configurations"
        ordering = ['service_type', 'country_or_provider']
        unique_together = ('country_or_provider', 'service_type')

class CheckLog(models.Model):
    """
    Records every time a status check was actually performed —
    i.e. when staff clicked through to an official verification
    website, or ran a Manpower search. This lets Admin (who doesn't
    do this work personally) see how many checks staff performed
    today, broken down by type.
    """

    class CheckType(models.TextChoices):
        VISA = 'VISA', 'Visa'
        PASSPORT = 'PASSPORT', 'Passport'
        AIR_TICKET = 'AIR_TICKET', 'Air Ticket'
        MANPOWER = 'MANPOWER', 'Manpower'

    check_type = models.CharField(max_length=20, choices=CheckType.choices)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='check_logs_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_check_type_display()} check by {self.created_by} at {self.created_at}"

    class Meta:
        verbose_name = "Check Log"
        verbose_name_plural = "Check Logs"
        ordering = ['-created_at']        