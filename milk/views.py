from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from core.models import SiteSettings
from .models import MilkProduct, MilkPurchase
from .forms import MilkProductForm, MilkPurchaseForm


def _base_context(request, active_menu):
    """
    Shared context builder used by every view in this app,
    so sidebar/topbar always get the info they need.
    """
    return {
        'site_settings': SiteSettings.get_settings(),
        'is_admin': request.user.is_admin_role(),
        'active_menu': active_menu,
    }


@login_required
def product_list_view(request):
    """
    Shows all Milk Products (active first, then inactive).
    Both Admin and Staff can view this page.
    """
    products = MilkProduct.objects.all()

    context = _base_context(request, 'milk')
    context['products'] = products
    return render(request, 'milk/product_list.html', context)


@login_required
def product_add_view(request):
    """
    'Add New Product' page.
    Both Admin and Staff can add a product — this is a simple
    operational task, not a sensitive one like Profit.
    """
    if request.method == 'POST':
        form = MilkProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, f'Product "{product.name}" added successfully.')
            return redirect('milk:product_list')
    else:
        form = MilkProductForm()

    context = _base_context(request, 'milk')
    context['form'] = form
    context['is_edit'] = False
    return render(request, 'milk/product_form.html', context)


@login_required
def product_edit_view(request, pk):
    """
    Edit an existing Milk Product's name or active status.
    """
    product = get_object_or_404(MilkProduct, pk=pk)

    if request.method == 'POST':
        form = MilkProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully.')
            return redirect('milk:product_list')
    else:
        form = MilkProductForm(instance=product)

    context = _base_context(request, 'milk')
    context['form'] = form
    context['is_edit'] = True
    context['product'] = product
    return render(request, 'milk/product_form.html', context)
@login_required
def purchase_list_view(request):
    """
    Shows all purchase records, most recent first.
    """
    purchases = MilkPurchase.objects.select_related('product', 'created_by').all()

    context = _base_context(request, 'milk')
    context['purchases'] = purchases
    return render(request, 'milk/purchase_list.html', context)


@login_required
def purchase_add_view(request):
    """
    'Milk Purchase' entry form.
    Saving this form does two things safely together
    (wrapped in a transaction so both succeed or both fail):
      1. Creates the MilkPurchase record.
      2. Stock automatically reflects the new purchase, because
         stock is calculated live from all Purchase/Sale records
         (see the Stock view in the next phase) — so no separate
         stock number needs to be updated manually here.
    """
    if request.method == 'POST':
        form = MilkPurchaseForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                purchase = form.save(commit=False)
                purchase.created_by = request.user
                purchase.save()
            messages.success(
                request,
                f'Purchase recorded: {purchase.quantity_bags} bags of '
                f'{purchase.product.name} — Total ৳{purchase.total_amount}'
            )
            return redirect('milk:purchase_list')
    else:
        form = MilkPurchaseForm()

    context = _base_context(request, 'milk')
    context['form'] = form
    return render(request, 'milk/purchase_form.html', context)