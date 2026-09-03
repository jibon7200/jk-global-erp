from django import forms


class PDFMultiUploadForm(forms.Form):
    """
    Allows selecting multiple PDF files at once — this is what
    enables Merge (uploading 2+ files combines their pages into
    one project).
    """
    files = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'accept': 'application/pdf'})
    )