from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import SiteSettings


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
    }
    return render(request, 'core/dashboard.html', context)
