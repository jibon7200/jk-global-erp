from datetime import timedelta, date
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from milk.models import MilkPurchase, MilkSale
from travel.models import AirTicket, Visa, Passport, Manpower
from expenses.models import Expense

from .models import SiteSettings
from .decorators import admin_required


@login_required
def dashboard_view(request):
    """
    Main dashboard shown right after login.
    Currently a simple placeholder — full dashboard cards
    (Milk stock, Today's sales, Ticket/Visa/Passport counts,
    Expenses) will be added in a later phase.

    IMPORTANT: Profit is NEVER shown here, even for Admin.
    Profit only appears on its own protected page.
    """
    site_settings = SiteSettings.get_settings()

    context = {
        'site_settings': site_settings,
        'is_admin': request.user.is_admin_role(),
        'active_menu': 'dashboard',
    }
    return render(request, 'core/dashboard.html', context)
def _resolve_date_range(request):
    """
    Reads the 'filter' query parameter (?filter=today, this_month, etc.)
    and returns (start_date, end_date, filter_label) for that range.
    Defaults to 'This Month' if nothing is specified.
    """
    today = timezone.localdate()
    filter_type = request.GET.get('filter', 'this_month')

    if filter_type == 'today':
        return today, today, 'Today'

    if filter_type == 'yesterday':
        y = today - timedelta(days=1)
        return y, y, 'Yesterday'

    if filter_type == 'last_month':
        first_of_this_month = today.replace(day=1)
        last_day_last_month = first_of_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        return first_day_last_month, last_day_last_month, 'Last Month'

    if filter_type == 'this_year':
        return today.replace(month=1, day=1), today, 'This Year'

    if filter_type == 'custom':
        start_str = request.GET.get('start_date')
        end_str = request.GET.get('end_date')
        if start_str and end_str:
            try:
                start_date = date.fromisoformat(start_str)
                end_date = date.fromisoformat(end_str)
                return start_date, end_date, 'Custom Range'
            except ValueError:
                pass
        # Fall through to This Month if custom dates are missing/invalid
        return today.replace(day=1), today, 'This Month'

    # Default: 'this_month'
    return today.replace(day=1), today, 'This Month'


def _calculate_milk_profit(start_date, end_date):
    """
    Calculates Milk Business profit using the Weighted Average Cost method:

    1. Average Cost per Bag = (Total amount ever purchased) / (Total bags ever purchased)
       -- calculated from ALL purchase history, not limited to the date range,
          because the cost basis of today's stock depends on everything bought so far.

    2. Sales Revenue (within date range) = sum of total_amount from Sale records in range.

    3. Cost of Goods Sold (COGS) = (bags sold within date range) x (Average Cost per Bag)

    4. Milk Profit = Sales Revenue - COGS
    """
    total_purchased_bags = MilkPurchase.objects.aggregate(
        total=Sum('quantity_bags')
    )['total'] or 0

    total_purchased_amount = MilkPurchase.objects.aggregate(
        total=Sum('total_amount')
    )['total'] or Decimal('0.00')

    if total_purchased_bags > 0:
        avg_cost_per_bag = total_purchased_amount / Decimal(total_purchased_bags)
    else:
        avg_cost_per_bag = Decimal('0.00')

    sales_in_range = MilkSale.objects.filter(date__range=[start_date, end_date])

    sold_bags_in_range = sales_in_range.aggregate(
        total=Sum('quantity_bags')
    )['total'] or 0

    sales_revenue_in_range = sales_in_range.aggregate(
        total=Sum('total_amount')
    )['total'] or Decimal('0.00')

    cogs = Decimal(sold_bags_in_range) * avg_cost_per_bag
    milk_profit = sales_revenue_in_range - cogs

    return milk_profit


@login_required
@admin_required
def profit_view(request):
    """
    THE PROFIT PAGE — Admin only.
    Protected at TWO levels:
      1. @login_required -> must be logged in.
      2. @admin_required -> must have role='ADMIN', otherwise 403 Forbidden,
         even if the URL is typed directly into the browser.

    Shows each business's profit separately, plus one combined
    TOTAL BUSINESS PROFIT, for a selected date range.
    """
    start_date, end_date, filter_label = _resolve_date_range(request)

    milk_profit = _calculate_milk_profit(start_date, end_date)

    ticket_profit = AirTicket.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(total=Sum('profit'))['total'] or Decimal('0.00')

    visa_profit = Visa.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(total=Sum('profit'))['total'] or Decimal('0.00')

    passport_profit = Passport.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(total=Sum('profit'))['total'] or Decimal('0.00')

    manpower_profit = Manpower.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(total=Sum('profit'))['total'] or Decimal('0.00')

    total_expenses = Expense.objects.filter(
        date__range=[start_date, end_date]
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    total_business_profit = (
        milk_profit + ticket_profit + visa_profit +
        passport_profit + manpower_profit - total_expenses
    )

    context = {
        'site_settings': SiteSettings.get_settings(),
        'is_admin': True,
        'active_menu': 'profit',
        'filter_label': filter_label,
        'start_date': start_date,
        'end_date': end_date,
        'milk_profit': milk_profit,
        'ticket_profit': ticket_profit,
        'visa_profit': visa_profit,
        'passport_profit': passport_profit,
        'manpower_profit': manpower_profit,
        'total_expenses': total_expenses,
        'total_business_profit': total_business_profit,
    }
    return render(request, 'core/profit.html', context)