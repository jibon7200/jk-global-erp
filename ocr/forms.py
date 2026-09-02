from django import forms
from .models import PassportScan


class PassportUploadForm(forms.Form):
    """Simple form for uploading a passport image to scan."""
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': 'image/*'})
    )


class PassportReviewForm(forms.ModelForm):
    """
    Shown AFTER OCR extraction, pre-filled with whatever was detected.
    The user can correct any mistakes here before confirming/saving —
    this is the mandatory 'Review' step required by the project spec.
    """

    class Meta:
        model = PassportScan
        fields = [
            'full_name', 'passport_number', 'nationality',
            'date_of_birth', 'date_of_expiry', 'sex'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-input'}),
            'nationality': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. BGD'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'DD-MM-YYYY'}),
            'date_of_expiry': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'DD-MM-YYYY'}),
            'sex': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'M / F'}),
        }