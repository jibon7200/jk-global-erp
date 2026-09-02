from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from core.models import SiteSettings
from .models import Expense
from .forms import ExpenseForm


def _base_context(request, active_menu):
    return {
        'site_settings': SiteSettings.get_settings(),
        'is_admin': request.user.is_admin_role(),
        'active_menu': active_menu,
    }


@login_required
def expense_list_view(request):
    """
    Shows all expense records. Both Admin and Staff can view and
    add expenses — this is operational data, not sensitive profit
    information, so no restriction is needed here.
    """
    expenses = Expense.objects.select_related('created_by').all()

    context = _base_context(request, 'expenses')
    context['expenses'] = expenses
    return render(request, 'expenses/expense_list.html', context)


@login_required
def expense_add_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.created_by = request.user
            expense.save()
            messages.success(
                request,
                f'Expense recorded: {expense.get_category_display()} — ৳{expense.amount}'
            )
            return redirect('expenses:expense_list')
    else:
        form = ExpenseForm()

    context = _base_context(request, 'expenses')
    context['form'] = form
    return render(request, 'expenses/expense_form.html', context)


@login_required
def expense_edit_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense record updated.')
            return redirect('expenses:expense_list')
    else:
        form = ExpenseForm(instance=expense)

    context = _base_context(request, 'expenses')
    context['form'] = form
    context['is_edit'] = True
    context['expense'] = expense
    return render(request, 'expenses/expense_form.html', context)
