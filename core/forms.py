from django import forms
from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['company_name', 'managing_director_name', 'logo', 'currency_symbol']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-input'}),
            'managing_director_name': forms.TextInput(attrs={'class': 'form-input'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
            'currency_symbol': forms.TextInput(attrs={'class': 'form-input'}),
        }