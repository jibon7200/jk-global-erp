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

class ThemeForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['theme_primary_color', 'theme_accent_color', 'theme_text_color', 'theme_background_color']
        widgets = {
            'theme_primary_color': forms.TextInput(attrs={'type': 'color', 'style': 'width:70px; height:42px; border:none; padding:0; cursor:pointer;'}),
            'theme_accent_color': forms.TextInput(attrs={'type': 'color', 'style': 'width:70px; height:42px; border:none; padding:0; cursor:pointer;'}),
            'theme_text_color': forms.TextInput(attrs={'type': 'color', 'style': 'width:70px; height:42px; border:none; padding:0; cursor:pointer;'}),
            'theme_background_color': forms.TextInput(attrs={'type': 'color', 'style': 'width:70px; height:42px; border:none; padding:0; cursor:pointer;'}),
        }        