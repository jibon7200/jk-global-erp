from django import forms


class DocumentUploadForm(forms.Form):
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': 'image/*'})
    )