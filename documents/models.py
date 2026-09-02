from django.db import models
from django.conf import settings


class DocumentEdit(models.Model):
    """
    Represents one document-editing session:
    an uploaded image, the text blocks OCR detected on it
    (with their position), and the user's edited version of
    that text. The original image is NEVER modified — exporting
    always creates a new file.
    """

    original_image = models.ImageField(upload_to='documents/originals/')

    detected_blocks = models.JSONField(
        default=list,
        help_text="List of {text, left, top, width, height} from OCR."
    )

    edited_blocks = models.JSONField(
        default=list,
        help_text="Same structure as detected_blocks, but with user corrections."
    )

    exported_file = models.FileField(
        upload_to='documents/exports/',
        blank=True,
        null=True,
        help_text="The saved edited copy, once exported."
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='document_edits_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Document Edit #{self.pk}"

    class Meta:
        verbose_name = "Document Edit"
        verbose_name_plural = "Document Edits"
        ordering = ['-created_at']
