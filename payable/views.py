from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from core.models import SiteSettings
from .models import Supplier, SupplierCharge, SupplierPayment
from .forms import SupplierForm, SupplierChargeForm, SupplierPaymentForm


def _base_context(request, active_menu):
    return {
        'site_settings': SiteSettings.get_settings(),
        'is_admin': request.user.is_admin_role(),
        'active_menu': active_menu,
    }


@login_required
def supplier_list_view(request):
    suppliers = Supplier.objects.all()
    rows = []
    total_payable = 0
    for s in suppliers:
        payable = s.get_current_payable()
        rows.append({'supplier': s, 'payable': payable})
        total_payable += payable

    context = _base_context(request, 'payable')
    context['rows'] = rows
    context['total_payable'] = total_payable
    return render(request, 'payable/supplier_list.html', context)


@login_required
def supplier_add_view(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.created_by = request.user
            supplier.save()
            messages.success(request, f'Supplier "{supplier.name}" added.')
            return redirect('payable:supplier_list')
    else:
        form = SupplierForm()

    context = _base_context(request, 'payable')
    context['form'] = form
    return render(request, 'payable/supplier_form.html', context)


@login_required
def supplier_detail_view(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    charges = list(supplier.charges.all())
    payments = list(supplier.payments.all())

    ledger = []
    for c in charges:
        ledger.append({'date': c.date, 'type': 'Owed', 'description': c.description, 'amount': c.amount, 'created_at': c.created_at})
    for p in payments:
        ledger.append({'date': p.date, 'type': 'Paid', 'description': p.note or 'Payment made', 'amount': -p.amount, 'created_at': p.created_at})
    ledger.sort(key=lambda row: (row['date'], row['created_at']), reverse=True)

    context = _base_context(request, 'payable')
    context['supplier'] = supplier
    context['ledger'] = ledger
    context['current_payable'] = supplier.get_current_payable()
    return render(request, 'payable/supplier_detail.html', context)


@login_required
def charge_add_view(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierChargeForm(request.POST)
        if form.is_valid():
            charge = form.save(commit=False)
            charge.supplier = supplier
            charge.created_by = request.user
            charge.save()
            messages.success(request, f'Charge of ৳{charge.amount} added for {supplier.name}.')
            return redirect('payable:supplier_detail', pk=supplier.pk)
    else:
        form = SupplierChargeForm()

    context = _base_context(request, 'payable')
    context['form'] = form
    context['supplier'] = supplier
    context['form_type'] = 'charge'
    return render(request, 'payable/transaction_form.html', context)


@login_required
def payment_add_view(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.supplier = supplier
            payment.created_by = request.user
            payment.save()
            messages.success(request, f'Payment of ৳{payment.amount} recorded for {supplier.name}.')
            return redirect('payable:supplier_detail', pk=supplier.pk)
    else:
        form = SupplierPaymentForm()

    context = _base_context(request, 'payable')
    context['form'] = form
    context['supplier'] = supplier
    context['form_type'] = 'payment'
    return render(request, 'payable/transaction_form.html', context)


@login_required
def payable_report_view(request):
    """
    Date-wise report: every payment WE made to suppliers.
    """
    payments = SupplierPayment.objects.select_related('supplier', 'created_by').all()
    context = _base_context(request, 'payable')
    context['payments'] = payments
    return render(request, 'payable/report.html', context)
