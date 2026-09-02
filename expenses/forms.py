from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    """
    Simple form for recording an office/business expense.
    """

    class Meta:
        model = Expense
        fields = ['date', 'category', 'amount', 'note']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'min': '0.01', 'step': '0.01'}),
            'note': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. August Office Rent'}),
        }