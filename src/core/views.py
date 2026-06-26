from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from tickets.models import Ticket


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    tickets = Ticket.objects.visible_for_user(request.user)
    context = {
        'open_count': tickets.filter(status__name='Abierto').count(),
        'in_progress_count': tickets.filter(status__name='En progreso').count(),
        'closed_count': tickets.filter(status__name='Cerrado').count(),
        'recent_tickets': tickets[:5],
    }
    return render(request, 'core/dashboard.html', context)
