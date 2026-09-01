from django import forms
from .models import MilkProduct, MilkPurchase


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
class MilkPurchaseForm(forms.ModelForm):
    """
    Form for recording a milk powder purchase.
    Only shows ACTIVE products in the dropdown.
    """

    class Meta:
        model = MilkPurchase
        fields = ['product', 'date', 'quantity_bags', 'price_per_bag']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-input'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'quantity_bags': forms.NumberInput(attrs={'class': 'form-input', 'min': '1'}),
            'price_per_bag': forms.NumberInput(attrs={'class': 'form-input', 'min': '0.01', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active products, so old discontinued products
        # don't clutter the purchase form.
        self.fields['product'].queryset = MilkProduct.objects.filter(is_active=True)


