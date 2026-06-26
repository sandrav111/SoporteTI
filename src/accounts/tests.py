from django.urls import reverse
from rest_framework.test import APIClient

from django.test import TestCase

from .models import User


class AuthenticationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user_returns_token(self):
        response = self.client.post(
            reverse('api-register'),
            {
                'full_name': 'Usuario Prueba',
                'username': 'usuario_prueba',
                'email': 'usuario@colegio.edu.co',
                'role': 'solicitante',
                'password': 'Segura123*',
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(username='usuario_prueba').exists())

    def test_login_returns_success_message(self):
        User.objects.create_user(
            username='tecnico1',
            full_name='Tecnico Uno',
            email='tecnico1@colegio.edu.co',
            password='Segura123*',
            role='tecnico',
        )

        response = self.client.post(
            reverse('api-login'),
            {'username': 'tecnico1', 'password': 'Segura123*'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Autenticacion satisfactoria.')

    def test_login_with_invalid_credentials_returns_error(self):
        User.objects.create_user(
            username='usuario_invalido',
            full_name='Usuario Invalido',
            email='usuario_invalido@colegio.edu.co',
            password='Segura123*',
            role='solicitante',
        )

        response = self.client.post(
            reverse('api-login'),
            {'username': 'usuario_invalido', 'password': 'otra-clave'},
            format='json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'Error en la autenticacion.')
