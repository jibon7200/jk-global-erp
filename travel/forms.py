from django import forms
from .models import AirTicket


class AirTicketForm(forms.ModelForm):
    """
    Form for recording an Air Ticket transaction.
    Note: 'profit' is NOT in this form — it's calculated
    automatically and never entered by the user.
    """

    class Meta:
        model = AirTicket
        fields = [
            'date', 'passport_holder_name', 'passport_number',
            'number_of_tickets', 'customer_payment', 'my_payment'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'passport_holder_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full name as in passport'}),
            'passport_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. AB1234567'}),
            'number_of_tickets': forms.NumberInput(attrs={'class': 'form-input', 'min': '1'}),
            'customer_payment': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'step': '0.01'}),
            'my_payment': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'step': '0.01'}),
        }