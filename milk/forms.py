from django import forms
from .models import MilkProduct


class MilkProductForm(forms.ModelForm):
    """
    Simple form to add or edit a Milk Product.
    Used by both the 'Add New Product' and 'Edit Product' pages.
    """

    class Meta:
        model = MilkProduct
        fields = ['name', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. DANO Full Cream'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            }),
        }