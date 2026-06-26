from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        REQUESTER = 'solicitante', 'Solicitante'
        TECHNICAL = 'tecnico', 'Tecnico'
        COORDINATOR = 'coordinador', 'Coordinador TI'
        ADMINISTRATOR = 'administrador', 'Administrador'

    full_name = models.CharField(max_length=150, verbose_name='Nombre completo')
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.REQUESTER)

    def __str__(self):
        return self.full_name or self.username
