from django.db import models
from django.conf import settings


class PDFProject(models.Model):
    """
    One PDF-editing 'workspace'. Pages can come from ONE OR MULTIPLE
    uploaded PDFs (this is how Merge works — pages from several
    source files get combined into a single ordered page list).
    Nothing is exported/saved as a final PDF until the user clicks
    Export — the original uploaded files are never modified.
    """

    pages = models.JSONField(
        default=list,
        help_text="Ordered list of: {id, source_file_id, page_number, rotation}"
    )

    exported_file = models.FileField(
        upload_to='pdf_editor/exports/',
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pdf_projects_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PDF Project #{self.pk}"

    class Meta:
        verbose_name = "PDF Project"
        verbose_name_plural = "PDF Projects"
        ordering = ['-created_at']


class PDFSourceFile(models.Model):
    """
    An original uploaded PDF file, kept unchanged, used as a source
    of pages for one PDFProject. A project can have several of these
    (that's what makes Merge possible).
    """

    project = models.ForeignKey(
        PDFProject,
        on_delete=models.CASCADE,
        related_name='source_files'
    )

    file = models.FileField(upload_to='pdf_editor/sources/')
    original_name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name