from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from core.models import SiteSettings
from .models import MilkProduct, MilkPurchase, MilkSale
from .forms import MilkProductForm, MilkPurchaseForm, MilkSaleForm


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
def _get_current_stock(product):
    """
    Calculates current stock for a single product LIVE from the
    database, by summing all purchases and subtracting all sales.
    This means stock never needs to be manually updated or stored
    separately — it's always accurate and derived from real transactions.
    """
    total_purchased = product.purchases.aggregate(total=Sum('quantity_bags'))['total'] or 0
    total_sold = product.sales.aggregate(total=Sum('quantity_bags'))['total'] or 0
    return total_purchased, total_sold, (total_purchased - total_sold)


@login_required
def sale_list_view(request):
    """
    Shows all sale records, most recent first.
    """
    sales = MilkSale.objects.select_related('product', 'created_by').all()

    context = _base_context(request, 'milk')
    context['sales'] = sales
    return render(request, 'milk/sale_list.html', context)


@login_required
def sale_add_view(request):
    """
    'Milk Sale' entry form.
    Before saving, checks that enough stock is available —
    this prevents an invalid stock operation (selling more than
    what's actually in stock), as required by the project spec.
    """
    if request.method == 'POST':
        form = MilkSaleForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            requested_qty = form.cleaned_data['quantity_bags']

            _, _, available_stock = _get_current_stock(product)

            if requested_qty > available_stock:
                messages.error(
                    request,
                    f'Cannot sell {requested_qty} bags of {product.name}. '
                    f'Only {available_stock} bags are currently in stock.'
                )
            else:
                with transaction.atomic():
                    sale = form.save(commit=False)
                    sale.created_by = request.user
                    sale.save()
                messages.success(
                    request,
                    f'Sale recorded: {sale.quantity_bags} bags of '
                    f'{sale.product.name} — Total ৳{sale.total_amount}'
                )
                return redirect('milk:sale_list')
    else:
        form = MilkSaleForm()

    context = _base_context(request, 'milk')
    context['form'] = form
    return render(request, 'milk/sale_form.html', context)


@login_required
def stock_view(request):
    """
    Shows current stock for every product, calculated live from
    Purchase and Sale records. Nothing here is manually entered —
    it's all derived automatically, as required by the project spec.
    """
    products = MilkProduct.objects.all()
    stock_data = []

    for product in products:
        total_purchased, total_sold, available = _get_current_stock(product)
        stock_data.append({
            'product': product,
            'total_purchased': total_purchased,
            'total_sold': total_sold,
            'available': available,
        })

    context = _base_context(request, 'milk')
    context['stock_data'] = stock_data
    return render(request, 'milk/stock.html', context)