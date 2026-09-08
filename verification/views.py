from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from core.models import SiteSettings
from travel.models import Manpower
from .models import VerificationConfig, CheckLog


def _base_context(request, active_menu):
    return {
        'site_settings': SiteSettings.get_settings(),
        'is_admin': request.user.is_admin_role(),
        'active_menu': active_menu,
    }


@login_required
def status_home_view(request):
    today = timezone.localdate()
    today_logs = CheckLog.objects.filter(created_at__date=today)

    todays_counts = {
        'visa': today_logs.filter(check_type=CheckLog.CheckType.VISA).count(),
        'passport': today_logs.filter(check_type=CheckLog.CheckType.PASSPORT).count(),
        'air_ticket': today_logs.filter(check_type=CheckLog.CheckType.AIR_TICKET).count(),
        'manpower': today_logs.filter(check_type=CheckLog.CheckType.MANPOWER).count(),
    }

    context = _base_context(request, 'status')
    context['todays_counts'] = todays_counts
    context['todays_total'] = sum(todays_counts.values())
    return render(request, 'verification/status_home.html', context)


def _handle_country_based_check(request, service_type, template_name):
    configs = VerificationConfig.objects.filter(service_type=service_type, is_active=True)
    selected_config = None
    result = None
    display_fields = []
    url1_valid = False
    url2_valid = False

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
        url1_valid = selected_config.official_url_1.startswith('http')
        url2_valid = selected_config.official_url_2.startswith('http')

    if request.method == 'POST' and selected_config:
        result = {
            'status': 'Manual Verification Required',
            'message': 'This system does not have official government/airline API access yet. Use the official website(s) below to verify manually.',
        }

    context = _base_context(request, 'status')
    context['configs'] = configs
    context['selected_config'] = selected_config
    context['display_fields'] = display_fields
    context['result'] = result
    context['url1_valid'] = url1_valid
    context['url2_valid'] = url2_valid
    return render(request, template_name, context)


@login_required
def visa_check_view(request):
    return _handle_country_based_check(request, VerificationConfig.ServiceType.VISA, 'verification/visa_check.html')


@login_required
def passport_check_view(request):
    show_result_prompt = request.method == 'POST'
    if show_result_prompt:
        CheckLog.objects.create(check_type=CheckLog.CheckType.PASSPORT, created_by=request.user)

    context = _base_context(request, 'status')
    context['show_result_prompt'] = show_result_prompt
    context['official_url'] = 'https://www.epassport.gov.bd/authorization/application-status'
    return render(request, 'verification/passport_check.html', context)


@login_required
def air_ticket_check_view(request):
    return _handle_country_based_check(
        request, VerificationConfig.ServiceType.AIR_TICKET, 'verification/air_ticket_check.html'
    )


@login_required
def manpower_check_view(request):
    passport_number = request.GET.get('passport_number', '').strip()
    matches = None

    if passport_number:
        matches = Manpower.objects.filter(passport_number__iexact=passport_number)
        CheckLog.objects.create(check_type=CheckLog.CheckType.MANPOWER, created_by=request.user)

    context = _base_context(request, 'status')
    context['passport_number'] = passport_number
    context['matches'] = matches
    context['bmet_url'] = 'https://oc.bmet.gov.bd/'
    return render(request, 'verification/manpower_check.html', context)


@login_required
def track_click_view(request, service_type, pk, slot):
    """
    Logs a check event, then redirects to the chosen official
    website slot (1 or 2) for that country/airline.
    """
    config = get_object_or_404(VerificationConfig, pk=pk)

    type_map = {
        'visa': CheckLog.CheckType.VISA,
        'passport': CheckLog.CheckType.PASSPORT,
        'air_ticket': CheckLog.CheckType.AIR_TICKET,
    }
    check_type = type_map.get(service_type)
    if check_type:
        CheckLog.objects.create(check_type=check_type, created_by=request.user)

    target_url = config.official_url_1 if slot == '1' else config.official_url_2
    return redirect(target_url)


@login_required
def track_bmet_click_view(request):
    CheckLog.objects.create(check_type=CheckLog.CheckType.MANPOWER, created_by=request.user)
    return redirect('https://oc.bmet.gov.bd/')