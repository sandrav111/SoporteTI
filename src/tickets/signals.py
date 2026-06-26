from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Category, Priority, TicketStatus


@receiver(post_migrate)
def seed_reference_data(sender, **kwargs):
    if sender.name != 'tickets':
        return

    for name, description in [
        ('Hardware', 'Incidencias relacionadas con equipos o perifericos'),
        ('Software', 'Problemas con aplicaciones o licencias'),
        ('Conectividad', 'Fallas de internet o red interna'),
        ('Cuentas', 'Acceso a plataformas institucionales'),
    ]:
        Category.objects.get_or_create(name=name, defaults={'description': description})

    for name, level in [('Baja', 1), ('Media', 2), ('Alta', 3), ('Critica', 4)]:
        Priority.objects.get_or_create(name=name, defaults={'level': level})

    for name, order in [('Abierto', 1), ('En progreso', 2), ('Escalado', 3), ('Cerrado', 4)]:
        TicketStatus.objects.get_or_create(name=name, defaults={'order': order})
