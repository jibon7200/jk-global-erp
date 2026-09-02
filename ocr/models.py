from django.db import models
from django.conf import settings


class PassportScan(models.Model):
    """
    Stores each passport OCR scan attempt — the uploaded image and
    whatever data was extracted from it. This is a scanning HISTORY,
    not the actual Passport business record (that stays in the
    travel app's Passport model). The Admin/Staff manually copies
    the reviewed, corrected data into the real Passport/Visa/Ticket
    entry form after checking it here.
    """

    image = models.ImageField(upload_to='passport_scans/')

    raw_ocr_text = models.TextField(
        blank=True,
        help_text="The full raw text Tesseract extracted from the image."
    )

    full_name = models.CharField(max_length=200, blank=True)
    passport_number = models.CharField(max_length=50, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    date_of_birth = models.CharField(max_length=20, blank=True)
    date_of_expiry = models.CharField(max_length=20, blank=True)
    sex = models.CharField(max_length=5, blank=True)

    extraction_successful = models.BooleanField(
        default=False,
        help_text="True if MRZ lines were found and parsed successfully."
    )

    reviewed_and_confirmed = models.BooleanField(
        default=False,
        help_text="True once Admin/Staff has reviewed and confirmed the data is correct."
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='passport_scans_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name or f"Scan #{self.pk}"

    class Meta:
        verbose_name = "Passport Scan"
        verbose_name_plural = "Passport Scans"
        ordering = ['-created_at']
