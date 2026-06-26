from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from accounts.models import User

from .models import Category, Priority, Ticket, TicketNote, TicketStatus


class TicketFlowTests(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.requester = User.objects.create_user(
            username='solicitante1',
            full_name='Solicitante Uno',
            email='solicitante1@colegio.edu.co',
            password='Segura123*',
            role='solicitante',
        )
        self.technical = User.objects.create_user(
            username='tecnico2',
            full_name='Tecnico Dos',
            email='tecnico2@colegio.edu.co',
            password='Segura123*',
            role='tecnico',
        )
        self.category = Category.objects.get(name='Hardware')
        self.priority = Priority.objects.get(name='Alta')
        self.open_status = TicketStatus.objects.get(name='Abierto')
        self.in_progress_status = TicketStatus.objects.get(name='En progreso')
        self.closed_status = TicketStatus.objects.get(name='Cerrado')

    def test_authenticated_user_can_create_ticket_from_web_form(self):
        self.client.login(username='solicitante1', password='Segura123*')

        response = self.client.post(
            reverse('tickets:create'),
            {
                'title': 'Pantalla sin imagen',
                'description': 'El monitor del laboratorio no muestra imagen.',
                'category': self.category.id,
                'priority': self.priority.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        ticket = Ticket.objects.get(title='Pantalla sin imagen')
        self.assertEqual(ticket.requester, self.requester)
        self.assertEqual(ticket.status, self.open_status)

    def test_requester_only_sees_their_own_tickets(self):
        other_requester = User.objects.create_user(
            username='solicitante2',
            full_name='Solicitante Dos',
            email='solicitante2@colegio.edu.co',
            password='Segura123*',
            role='solicitante',
        )
        Ticket.objects.create(
            title='Falla de impresora',
            description='No imprime documentos',
            category=self.category,
            priority=self.priority,
            status=self.open_status,
            requester=self.requester,
        )
        Ticket.objects.create(
            title='Error en correo',
            description='No abre la bandeja institucional',
            category=self.category,
            priority=self.priority,
            status=self.open_status,
            requester=other_requester,
        )

        visible = Ticket.objects.visible_for_user(self.requester)

        self.assertEqual(visible.count(), 1)
        self.assertEqual(visible.first().requester, self.requester)

    def test_support_user_can_add_note_from_web(self):
        ticket = Ticket.objects.create(
            title='Teclado con falla',
            description='Varias teclas no responden',
            category=self.category,
            priority=self.priority,
            status=self.open_status,
            requester=self.requester,
            assigned_to=self.technical,
        )

        self.client.login(username='tecnico2', password='Segura123*')
        response = self.client.post(
            reverse('tickets:add-note', kwargs={'pk': ticket.pk}),
            {'content': 'Se programo revision presencial del equipo.'},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(TicketNote.objects.filter(ticket=ticket, author=self.technical).exists())

    def test_support_user_can_close_ticket_from_web(self):
        ticket = Ticket.objects.create(
            title='Falla en red de aula',
            description='No hay acceso a internet en el aula 3.',
            category=self.category,
            priority=self.priority,
            status=self.open_status,
            requester=self.requester,
            assigned_to=self.technical,
        )

        self.client.login(username='tecnico2', password='Segura123*')
        response = self.client.post(
            reverse('tickets:close', kwargs={'pk': ticket.pk}),
            {'feedback': 'Se reinicio el switch y el servicio quedo operativo.'},
        )

        ticket.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ticket.status, self.closed_status)
        self.assertEqual(ticket.feedback, 'Se reinicio el switch y el servicio quedo operativo.')
        self.assertIsNotNone(ticket.closed_at)

    def test_requester_cannot_close_ticket_from_web(self):
        ticket = Ticket.objects.create(
            title='Error en proyector',
            description='El proyector no muestra imagen.',
            category=self.category,
            priority=self.priority,
            status=self.open_status,
            requester=self.requester,
        )

        self.client.login(username='solicitante1', password='Segura123*')
        response = self.client.post(reverse('tickets:close', kwargs={'pk': ticket.pk}), {'feedback': 'Intento cerrar'})

        self.assertEqual(response.status_code, 403)

    def test_frontend_pages_render_for_authenticated_user(self):
        ticket = Ticket.objects.create(
            title='Software bloqueado',
            description='La aplicacion academica no abre.',
            category=self.category,
            priority=self.priority,
            status=self.open_status,
            requester=self.requester,
        )

        self.client.login(username='solicitante1', password='Segura123*')

        dashboard_response = self.client.get(reverse('core:dashboard'))
        list_response = self.client.get(reverse('tickets:list'))
        detail_response = self.client.get(reverse('tickets:detail', kwargs={'pk': ticket.pk}))

        self.assertEqual(dashboard_response.status_code, 200)
        self.assertContains(dashboard_response, 'Panel principal')
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, 'Tickets')
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, ticket.title)

    def test_api_requires_authentication_for_ticket_list(self):
        response = self.api_client.get(reverse('api-ticket-list'))

        self.assertEqual(response.status_code, 401)

    def test_requester_can_create_ticket_through_api(self):
        token = Token.objects.create(user=self.requester)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.api_client.post(
            reverse('api-ticket-list'),
            {
                'title': 'Problema con internet',
                'description': 'No carga el portal institucional.',
                'category': self.category.id,
                'priority': self.priority.id,
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Ticket.objects.filter(title='Problema con internet', requester=self.requester).exists())

    def test_requester_only_receives_their_tickets_in_api_list(self):
        other_requester = User.objects.create_user(
            username='solicitante3',
            full_name='Solicitante Tres',
            email='solicitante3@colegio.edu.co',
            password='Segura123*',
            role='solicitante',
        )
        Ticket.objects.create(
            title='Caso propio',
            description='Descripcion 1',
            category=self.category,
            priority=self.priority,
            status=self.open_status,
            requester=self.requester,
        )
        Ticket.objects.create(
            title='Caso ajeno',
            description='Descripcion 2',
            category=self.category,
            priority=self.priority,
            status=self.open_status,
            requester=other_requester,
        )

        token = Token.objects.create(user=self.requester)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = self.api_client.get(reverse('api-ticket-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Caso propio')

    def test_requester_cannot_change_ticket_status_from_api(self):
        ticket = Ticket.objects.create(
            title='Acceso a wifi',
            description='No conecta al wifi institucional.',
            category=self.category,
            priority=self.priority,
            status=self.open_status,
            requester=self.requester,
        )
        token = Token.objects.create(user=self.requester)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.api_client.patch(
            reverse('api-ticket-status', kwargs={'pk': ticket.pk}),
            {'status': self.in_progress_status.id},
            format='json',
        )

        ticket.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(ticket.status, self.open_status)

    def test_support_user_can_change_ticket_status_from_api(self):
        ticket = Ticket.objects.create(
            title='Correo sin acceso',
            description='No abre la cuenta institucional.',
            category=self.category,
            priority=self.priority,
            status=self.open_status,
            requester=self.requester,
            assigned_to=self.technical,
        )
        token = Token.objects.create(user=self.technical)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.api_client.patch(
            reverse('api-ticket-status', kwargs={'pk': ticket.pk}),
            {'status': self.in_progress_status.id, 'feedback': 'Caso tomado por soporte.'},
            format='json',
        )

        ticket.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ticket.status, self.in_progress_status)
        self.assertEqual(ticket.feedback, 'Caso tomado por soporte.')

    def test_authenticated_user_can_add_note_through_api(self):
        ticket = Ticket.objects.create(
            title='Actualizacion pendiente',
            description='El equipo necesita actualizacion de software.',
            category=self.category,
            priority=self.priority,
            status=self.open_status,
            requester=self.requester,
        )
        token = Token.objects.create(user=self.requester)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.api_client.post(
            reverse('api-ticket-notes', kwargs={'pk': ticket.pk}),
            {'content': 'Se agrega informacion adicional del caso.'},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(TicketNote.objects.filter(ticket=ticket, author=self.requester).exists())

    def test_requester_cannot_update_assigned_to_through_api(self):
        ticket = Ticket.objects.create(
            title='Equipo lento',
            description='El equipo tarda mucho en iniciar.',
            category=self.category,
            priority=self.priority,
            status=self.open_status,
            requester=self.requester,
        )
        token = Token.objects.create(user=self.requester)
        self.api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

        response = self.api_client.patch(
            reverse('api-ticket-detail', kwargs={'pk': ticket.pk}),
            {'assigned_to': self.technical.id, 'status': self.in_progress_status.id},
            format='json',
        )

        ticket.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(ticket.assigned_to)
        self.assertEqual(ticket.status, self.open_status)
