from django.core.management.base import BaseCommand

from accounts.models import User

from tickets.models import Category, Priority, Ticket, TicketStatus


class Command(BaseCommand):
    help = 'Crea datos de ejemplo'

    def handle(self, *args, **options):
        requester, _ = User.objects.get_or_create(
            username='solicitante_demo',
            defaults={
                'full_name': 'Solicitante Demo',
                'email': 'solicitante_demo@colegio.edu.co',
                'role': 'solicitante',
            },
        )
        requester.set_password('Demo1234*')
        requester.save()

        technical, _ = User.objects.get_or_create(
            username='tecnico_demo',
            defaults={
                'full_name': 'Tecnico Demo',
                'email': 'tecnico_demo@colegio.edu.co',
                'role': 'tecnico',
            },
        )
        technical.set_password('Demo1234*')
        technical.save()

        open_status = TicketStatus.objects.get(name='Abierto')
        hardware = Category.objects.get(name='Hardware')
        high_priority = Priority.objects.get(name='Alta')

        Ticket.objects.get_or_create(
            title='Computador del aula no enciende',
            requester=requester,
            defaults={
                'description': 'El equipo asignado al aula 204 no responde al intentar encenderlo.',
                'category': hardware,
                'priority': high_priority,
                'status': open_status,
                'assigned_to': technical,
            },
        )

        self.stdout.write(self.style.SUCCESS('Datos de ejemplo creados correctamente.'))
