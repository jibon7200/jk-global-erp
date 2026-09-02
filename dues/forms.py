from django import forms
from .models import Customer, DueCharge, DuePayment


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone_number', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Customer full name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 01712345678'}),
            'notes': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Optional note'}),
        }


class DueChargeForm(forms.ModelForm):
    class Meta:
        model = DueCharge
        fields = ['date', 'description', 'amount']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'description': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. 5 bags milk powder on credit'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'min': '0.01', 'step': '0.01'}),
        }


class DuePaymentForm(forms.ModelForm):
    class Meta:
        model = DuePayment
        fields = ['date', 'amount', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'min': '0.01', 'step': '0.01'}),
            'note': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Optional note'}),
        }