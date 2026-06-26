from django.utils import timezone

from .models import Ticket, TicketNote, TicketStatus


def get_open_status():
    return TicketStatus.objects.get(name='Abierto')


def create_ticket_from_form(form, requester):
    ticket = form.save(commit=False)
    ticket.requester = requester
    ticket.status = get_open_status()
    ticket.save()
    return ticket


def create_ticket_from_data(validated_data, requester):
    ticket = Ticket(**validated_data)
    ticket.requester = requester
    ticket.status = get_open_status()
    ticket.save()
    return ticket


def add_note_to_ticket(ticket, author, content):
    return TicketNote.objects.create(ticket=ticket, author=author, content=content)


def close_ticket(ticket, feedback=''):
    closed_status = TicketStatus.objects.get(name='Cerrado')
    ticket.status = closed_status
    ticket.feedback = feedback
    ticket.closed_at = timezone.now()
    ticket.save()
    return ticket
