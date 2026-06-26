from django.conf import settings
from django.db import models
from django.utils import timezone


class TicketQuerySet(models.QuerySet):
    def visible_for_user(self, user):
        if user.role == 'solicitante':
            return self.filter(requester=user)
        return self


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.name


class Priority(models.Model):
    name = models.CharField(max_length=50, unique=True)
    level = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ('level', 'name')
        verbose_name = 'Prioridad'
        verbose_name_plural = 'Prioridades'

    def __str__(self):
        return self.name


class TicketStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ('order', 'name')
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'

    def __str__(self):
        return self.name


class Ticket(models.Model):
    code = models.CharField(max_length=20, unique=True, blank=True)
    title = models.CharField(max_length=120)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='tickets')
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT, related_name='tickets')
    status = models.ForeignKey(TicketStatus, on_delete=models.PROTECT, related_name='tickets')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requested_tickets')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets',
    )
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    objects = TicketQuerySet.as_manager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return f'{self.code} - {self.title}'

    def save(self, *args, **kwargs):
        if not self.code:
            prefix = timezone.now().strftime('TCK%y%m')
            serial = Ticket.objects.filter(code__startswith=prefix).count() + 1
            self.code = f'{prefix}{serial:03d}'
        if self.status_id and self.status.name == 'Cerrado' and not self.closed_at:
            self.closed_at = timezone.now()
        if self.status_id and self.status.name != 'Cerrado':
            self.closed_at = None
        super().save(*args, **kwargs)


class TicketNote(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ticket_notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'

    def __str__(self):
        return f'Nota {self.id} - {self.ticket.code}'
