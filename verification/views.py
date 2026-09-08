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
    """
    Status Checking hub — also shows today's check counts per type,
    so Admin can see how much verification work staff has done today
    without having to ask.
    """
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
    """
    Bangladesh e-Passport application status checking ONLY —
    this tool answers 'is my new passport ready yet / how much
    longer will it take', using the applicant's Online Registration
    ID (OID) or Application ID plus Date of Birth, on the official
    epassport.gov.bd site. This is NOT for foreign passport
    verification (that would need each country's own system).
    """
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
    """
    First checks JK GLOBAL's own database (this is the primary,
    real capability). If nothing matches internally, this ALSO
    offers the official Bangladesh government BMET Smart Card
    verification portal as a fallback — a real, verified government
    system for checking manpower/emigration clearance status.
    """
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
def track_click_view(request, service_type, pk):
    """
    Logs a check event, then redirects the user on to the official
    verification website. This is the ONLY way the 'OPEN OFFICIAL
    VERIFICATION WEBSITE' button works now — clicking it always
    counts as one check for that category before sending the user
    onward.
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

    return redirect(config.official_url)


@login_required
def track_bmet_click_view(request):
    """
    Logs a Manpower check when the user clicks through to the
    official BMET government portal (used when no internal record
    was found), then redirects them there.
    """
    CheckLog.objects.create(check_type=CheckLog.CheckType.MANPOWER, created_by=request.user)
    return redirect('https://oc.bmet.gov.bd/')