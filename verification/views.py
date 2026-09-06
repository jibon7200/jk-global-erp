from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import SiteSettings
from travel.models import Manpower
from .models import VerificationConfig


def _base_context(request, active_menu):
    return {
        'site_settings': SiteSettings.get_settings(),
        'is_admin': request.user.is_admin_role(),
        'active_menu': active_menu,
    }


@login_required
def status_home_view(request):
    """
    The main Status Checking hub — four cards linking to each
    checking tool.
    """
    context = _base_context(request, 'status')
    return render(request, 'verification/status_home.html', context)


def _handle_country_based_check(request, service_type, template_name):
    configs = VerificationConfig.objects.filter(service_type=service_type, is_active=True)
    selected_config = None
    result = None
    display_fields = []

    country_id = request.GET.get('country') or request.POST.get('country')
    if country_id:
        selected_config = configs.filter(pk=country_id).first()

    if selected_config:
        for field in selected_config.required_fields:
            display_fields.append({
                'name': field['name'],
                'label': field['label'],
                'value': request.POST.get(field['name'], ''),
            })

    if request.method == 'POST' and selected_config:
        if selected_config.method == VerificationConfig.Method.WEBSITE:
            result = {
                'status': 'Manual Verification Required',
                'message': 'No official API is integrated for this country. Please use the official website below to verify manually.',
                'show_website_button': True,
            }
        elif selected_config.method == VerificationConfig.Method.API:
            result = {
                'status': 'Unable to Verify',
                'message': 'An official API is planned for this country but is not yet connected. Please verify manually via the official website.',
                'show_website_button': bool(selected_config.official_url),
            }
        else:
            result = {
                'status': 'Manual Verification Required',
                'message': 'This country requires manual verification. Please use the official website or contact the relevant authority.',
                'show_website_button': bool(selected_config.official_url),
            }

    context = _base_context(request, 'status')
    context['configs'] = configs
    context['selected_config'] = selected_config
    context['display_fields'] = display_fields
    context['result'] = result
    return render(request, template_name, context)


@login_required
def visa_check_view(request):
    return _handle_country_based_check(request, VerificationConfig.ServiceType.VISA, 'verification/visa_check.html')


@login_required
def passport_check_view(request):
    return _handle_country_based_check(request, VerificationConfig.ServiceType.PASSPORT, 'verification/passport_check.html')


@login_required
def air_ticket_check_view(request):
    """
    Air Ticket checking works the same way as Visa/Passport, but
    the "country" field is repurposed as Airline/Provider name.
    """
    return _handle_country_based_check(
        request, VerificationConfig.ServiceType.AIR_TICKET, 'verification/air_ticket_check.html'
    )


@login_required
def manpower_check_view(request):
    """
    Manpower Checking is DIFFERENT from the other three — it
    searches JK GLOBAL's OWN database of Manpower records, so it
    can give a real, honest result (not a placeholder), as allowed
    by the project spec (checking internal records first).
    Profit/cost is intentionally never shown here, even to Admin —
    this is a status lookup tool, not a financial report.
    """
    passport_number = request.GET.get('passport_number', '').strip()
    matches = None

    if passport_number:
        matches = Manpower.objects.filter(passport_number__iexact=passport_number)

    context = _base_context(request, 'status')
    context['passport_number'] = passport_number
    context['matches'] = matches
    return render(request, 'verification/manpower_check.html', context)
