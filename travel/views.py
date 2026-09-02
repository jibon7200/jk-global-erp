from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from core.models import SiteSettings
from .models import AirTicket, Visa, Passport, Manpower
from .forms import AirTicketForm, VisaForm, PassportForm, ManpowerForm


def _base_context(request, active_menu):
    """
    Shared context builder for sidebar/topbar,
    reused the same way as the milk app.
    """
    return {
        'site_settings': SiteSettings.get_settings(),
        'is_admin': request.user.is_admin_role(),
        'active_menu': active_menu,
    }


@login_required
def ticket_list_view(request):
    """
    Shows all Air Ticket records.
    IMPORTANT: The 'profit' field is deliberately NOT passed
    to the template context in a way Staff could see — the
    template itself checks is_admin before showing that column.
    """
    tickets = AirTicket.objects.select_related('created_by').all()

    context = _base_context(request, 'travel')
    context['tickets'] = tickets
    return render(request, 'travel/ticket_list.html', context)


@login_required
def ticket_add_view(request):
    """
    'Air Ticket' entry form.
    Both Admin and Staff can add a ticket record — this is a
    normal operational task. The profit is calculated
    automatically on save, but is only ever DISPLAYED to Admin.
    """
    if request.method == 'POST':
        form = AirTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            messages.success(
                request,
                f'Ticket record saved for {ticket.passport_holder_name}.'
            )
            return redirect('travel:ticket_list')
    else:
        form = AirTicketForm()

    context = _base_context(request, 'travel')
    context['form'] = form
    return render(request, 'travel/ticket_form.html', context)


@login_required
def ticket_edit_view(request, pk):
    """
    Edit an existing Air Ticket record.
    """
    ticket = get_object_or_404(AirTicket, pk=pk)

    if request.method == 'POST':
        form = AirTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ticket record for {ticket.passport_holder_name} updated.')
            return redirect('travel:ticket_list')
    else:
        form = AirTicketForm(instance=ticket)

    context = _base_context(request, 'travel')
    context['form'] = form
    context['is_edit'] = True
    context['ticket'] = ticket
    return render(request, 'travel/ticket_form.html', context)
# ============================================
# VISA VIEWS
# ============================================

@login_required
def visa_list_view(request):
    visas = Visa.objects.select_related('created_by').all()
    context = _base_context(request, 'travel')
    context['visas'] = visas
    return render(request, 'travel/visa_list.html', context)


@login_required
def visa_add_view(request):
    if request.method == 'POST':
        form = VisaForm(request.POST)
        if form.is_valid():
            visa = form.save(commit=False)
            visa.created_by = request.user
            visa.save()
            messages.success(request, f'Visa record saved for {visa.passport_holder_name}.')
            return redirect('travel:visa_list')
    else:
        form = VisaForm()

    context = _base_context(request, 'travel')
    context['form'] = form
    return render(request, 'travel/visa_form.html', context)


@login_required
def visa_edit_view(request, pk):
    visa = get_object_or_404(Visa, pk=pk)
    if request.method == 'POST':
        form = VisaForm(request.POST, instance=visa)
        if form.is_valid():
            form.save()
            messages.success(request, f'Visa record for {visa.passport_holder_name} updated.')
            return redirect('travel:visa_list')
    else:
        form = VisaForm(instance=visa)

    context = _base_context(request, 'travel')
    context['form'] = form
    context['is_edit'] = True
    context['visa'] = visa
    return render(request, 'travel/visa_form.html', context)


# ============================================
# PASSPORT VIEWS
# ============================================

@login_required
def passport_list_view(request):
    passports = Passport.objects.select_related('created_by').all()
    context = _base_context(request, 'travel')
    context['passports'] = passports
    return render(request, 'travel/passport_list.html', context)


@login_required
def passport_add_view(request):
    if request.method == 'POST':
        form = PassportForm(request.POST)
        if form.is_valid():
            passport = form.save(commit=False)
            passport.created_by = request.user
            passport.save()
            messages.success(request, f'Passport record saved for {passport.passport_holder_name}.')
            return redirect('travel:passport_list')
    else:
        form = PassportForm()

    context = _base_context(request, 'travel')
    context['form'] = form
    return render(request, 'travel/passport_form.html', context)


@login_required
def passport_edit_view(request, pk):
    passport = get_object_or_404(Passport, pk=pk)
    if request.method == 'POST':
        form = PassportForm(request.POST, instance=passport)
        if form.is_valid():
            form.save()
            messages.success(request, f'Passport record for {passport.passport_holder_name} updated.')
            return redirect('travel:passport_list')
    else:
        form = PassportForm(instance=passport)

    context = _base_context(request, 'travel')
    context['form'] = form
    context['is_edit'] = True
    context['passport'] = passport
    return render(request, 'travel/passport_form.html', context)


# ============================================
# MANPOWER VIEWS
# ============================================

@login_required
def manpower_list_view(request):
    manpower_records = Manpower.objects.select_related('created_by').all()
    context = _base_context(request, 'travel')
    context['manpower_records'] = manpower_records
    return render(request, 'travel/manpower_list.html', context)


@login_required
def manpower_add_view(request):
    if request.method == 'POST':
        form = ManpowerForm(request.POST)
        if form.is_valid():
            manpower = form.save(commit=False)
            manpower.created_by = request.user
            manpower.save()
            messages.success(request, f'Manpower record saved for {manpower.passport_holder_name}.')
            return redirect('travel:manpower_list')
    else:
        form = ManpowerForm()

    context = _base_context(request, 'travel')
    context['form'] = form
    return render(request, 'travel/manpower_form.html', context)


@login_required
def manpower_edit_view(request, pk):
    manpower = get_object_or_404(Manpower, pk=pk)
    if request.method == 'POST':
        form = ManpowerForm(request.POST, instance=manpower)
        if form.is_valid():
            form.save()
            messages.success(request, f'Manpower record for {manpower.passport_holder_name} updated.')
            return redirect('travel:manpower_list')
    else:
        form = ManpowerForm(instance=manpower)

    context = _base_context(request, 'travel')
    context['form'] = form
    context['is_edit'] = True
    context['manpower'] = manpower
    return render(request, 'travel/manpower_form.html', context)