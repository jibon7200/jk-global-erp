from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from core.models import SiteSettings


class CustomLoginView(LoginView):
    """
    Custom login page for JK GLOBAL.
    Uses our own template (accounts/login.html) instead of Django's
    default plain login page, so we can show the company logo,
    branding, and a modern design.
    """
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = SiteSettings.get_settings()
        return context

    def get_success_url(self):
        return '/dashboard/'


def custom_logout_view(request):
    """
    Logs the user out and sends them back to the login page
    with a clean, simple redirect (no confirmation page needed).
    """
    logout(request)
    return redirect('accounts:login')