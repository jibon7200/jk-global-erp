from django import forms
from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'company_name', 'managing_director_name', 'logo', 'currency_symbol',
            'dashboard_hero_image', 'milk_banner_image', 'travel_banner_image', 'expense_banner_image',
        ]
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
            'company_name': forms.TextInput(attrs={'class': 'form-input'}),
            'managing_director_name': forms.TextInput(attrs={'class': 'form-input'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
            'currency_symbol': forms.TextInput(attrs={'class': 'form-input'}),
            'dashboard_hero_image': forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': 'image/*,video/mp4,video/webm'}),
            'milk_banner_image': forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': 'image/*,video/mp4,video/webm'}),
            'travel_banner_image': forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': 'image/*,video/mp4,video/webm'}),
            'expense_banner_image': forms.ClearableFileInput(attrs={'class': 'form-input', 'accept': 'image/*,video/mp4,video/webm'}),
        }       