from django import forms
from .models import Supplier, SupplierCharge, SupplierPayment


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone_number', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Supplier/Partner name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'notes': forms.TextInput(attrs={'class': 'form-input'}),
        }


class SupplierChargeForm(forms.ModelForm):
    class Meta:
        model = SupplierCharge
        fields = ['date', 'description', 'amount']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 10 bags milk powder received on credit'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'min': '0.01', 'step': '0.01'}),
        }


class SupplierPaymentForm(forms.ModelForm):
    class Meta:
        model = SupplierPayment
        fields = ['date', 'amount', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'min': '0.01', 'step': '0.01'}),
            'note': forms.TextInput(attrs={'class': 'form-input'}),
        }