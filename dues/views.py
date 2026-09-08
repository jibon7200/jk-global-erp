from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from core.models import SiteSettings
from .models import Customer, DueCharge, DuePayment
from .forms import CustomerForm, DueChargeForm, DuePaymentForm


def _base_context(request, active_menu):
    return {
        'site_settings': SiteSettings.get_settings(),
        'is_admin': request.user.is_admin_role(),
        'active_menu': active_menu,
    }


@login_required
def customer_list_view(request):
    """
    Shows all customers with their current due, calculated live.
    """
    customers = Customer.objects.all()
    customer_rows = []
    total_outstanding = 0

    for customer in customers:
        due = customer.get_current_due()
        customer_rows.append({'customer': customer, 'due': due})
        total_outstanding += due

    context = _base_context(request, 'dues')
    context['customer_rows'] = customer_rows
    context['total_outstanding'] = total_outstanding
    return render(request, 'dues/customer_list.html', context)


@login_required
def customer_add_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.created_by = request.user
            customer.save()
            messages.success(request, f'Customer "{customer.name}" added.')
            return redirect('dues:customer_list')
    else:
        form = CustomerForm()

    context = _base_context(request, 'dues')
    context['form'] = form
    return render(request, 'dues/customer_form.html', context)


@login_required
def customer_detail_view(request, pk):
    """
    Shows a single customer's full ledger: all charges and payments,
    combined into one chronological history, with the running due
    shown at the top.
    """
    customer = get_object_or_404(Customer, pk=pk)

    charges = list(customer.charges.all())
    payments = list(customer.payments.all())

    ledger = []
    for c in charges:
        ledger.append({'date': c.date, 'type': 'Charge', 'description': c.description, 'amount': c.amount, 'created_at': c.created_at})
    for p in payments:
        ledger.append({'date': p.date, 'type': 'Payment', 'description': p.note or 'Payment received', 'amount': -p.amount, 'created_at': p.created_at})

    ledger.sort(key=lambda row: (row['date'], row['created_at']), reverse=True)

    context = _base_context(request, 'dues')
    context['customer'] = customer
    context['ledger'] = ledger
    context['current_due'] = customer.get_current_due()
    return render(request, 'dues/customer_detail.html', context)


@login_required
def charge_add_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = DueChargeForm(request.POST)
        if form.is_valid():
            charge = form.save(commit=False)
            charge.customer = customer
            charge.created_by = request.user
            charge.save()
            messages.success(request, f'Charge of ৳{charge.amount} added for {customer.name}.')
            return redirect('dues:customer_detail', pk=customer.pk)
    else:
        form = DueChargeForm()

    context = _base_context(request, 'dues')
    context['form'] = form
    context['customer'] = customer
    context['form_type'] = 'charge'
    return render(request, 'dues/transaction_form.html', context)


@login_required
def payment_add_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    if request.method == 'POST':
        form = DuePaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.customer = customer
            payment.created_by = request.user
            payment.save()
            messages.success(request, f'Payment of ৳{payment.amount} recorded for {customer.name}.')
            return redirect('dues:customer_detail', pk=customer.pk)
    else:
        form = DuePaymentForm()

    context = _base_context(request, 'dues')
    context['form'] = form
    context['customer'] = customer
    context['form_type'] = 'payment'
    return render(request, 'dues/transaction_form.html', context)

@login_required
def due_report_view(request):
    """Date-wise report of every payment RECEIVED from customers."""
    from .models import DuePayment
    payments = DuePayment.objects.select_related('customer', 'created_by').all()
    context = _base_context(request, 'dues')
    context['payments'] = payments
    return render(request, 'dues/report.html', context)