from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User

from .forms import SUPPORT_ROLES, TicketCreateForm, TicketNoteForm, TicketUpdateForm
from .models import Category, Priority, Ticket, TicketStatus
from .services import add_note_to_ticket, close_ticket, create_ticket_from_form


def _visible_tickets(user):
    return Ticket.objects.select_related(
        'requester', 'assigned_to', 'category', 'priority', 'status'
    ).prefetch_related('notes').visible_for_user(user)


def _is_support(user):
    return user.role in SUPPORT_ROLES


@login_required
def ticket_list(request):
    tickets = _visible_tickets(request.user)

    if status_id := request.GET.get('status'):
        tickets = tickets.filter(status_id=status_id)
    if priority_id := request.GET.get('priority'):
        tickets = tickets.filter(priority_id=priority_id)
    if category_id := request.GET.get('category'):
        tickets = tickets.filter(category_id=category_id)
    if search := request.GET.get('search'):
        tickets = tickets.filter(title__icontains=search)

    context = {
        'tickets': tickets,
        'statuses': TicketStatus.objects.all(),
        'priorities': Priority.objects.all(),
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'tickets/ticket_list.html', context)


@login_required
def ticket_create(request):
    form = TicketCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        ticket = create_ticket_from_form(form, request.user)
        messages.success(request, f'El ticket {ticket.code} fue creado correctamente.')
        return redirect('tickets:detail', pk=ticket.pk)
    return render(request, 'tickets/ticket_form.html', {'form': form, 'page_title': 'Crear ticket'})


@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(_visible_tickets(request.user), pk=pk)
    note_form = TicketNoteForm()
    return render(
        request,
        'tickets/ticket_detail.html',
        {
            'ticket': ticket,
            'note_form': note_form,
            'is_support': _is_support(request.user),
        },
    )


@login_required
def ticket_update(request, pk):
    ticket = get_object_or_404(_visible_tickets(request.user), pk=pk)
    form = TicketUpdateForm(request.POST or None, instance=ticket, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'El ticket fue actualizado correctamente.')
        return redirect('tickets:detail', pk=ticket.pk)
    return render(request, 'tickets/ticket_form.html', {'form': form, 'page_title': 'Actualizar ticket'})


@login_required
def ticket_delete(request, pk):
    ticket = get_object_or_404(_visible_tickets(request.user), pk=pk)
    if not (_is_support(request.user) or ticket.requester_id == request.user.id):
        return HttpResponseForbidden('No tienes permiso para eliminar este ticket.')

    if request.method == 'POST':
        code = ticket.code
        ticket.delete()
        messages.warning(request, f'El ticket {code} fue eliminado.')
        return redirect('tickets:list')
    return render(request, 'tickets/ticket_confirm_delete.html', {'ticket': ticket})


@login_required
def ticket_add_note(request, pk):
    ticket = get_object_or_404(_visible_tickets(request.user), pk=pk)
    form = TicketNoteForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        add_note_to_ticket(ticket=ticket, author=request.user, content=form.cleaned_data['content'])
        messages.success(request, 'La nota fue registrada correctamente.')
    return redirect('tickets:detail', pk=ticket.pk)


@login_required
def ticket_close(request, pk):
    ticket = get_object_or_404(_visible_tickets(request.user), pk=pk)
    if not _is_support(request.user):
        return HttpResponseForbidden('No tienes permiso para cerrar este ticket.')

    if request.method == 'POST':
        close_ticket(ticket, request.POST.get('feedback', ''))
        messages.success(request, 'El ticket fue cerrado correctamente.')
        return redirect('tickets:detail', pk=ticket.pk)
    return render(request, 'tickets/ticket_close.html', {'ticket': ticket})
