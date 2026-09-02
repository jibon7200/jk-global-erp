from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from core.models import SiteSettings
from .models import AirTicket
from .forms import AirTicketForm


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
