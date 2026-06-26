from django.contrib import admin

from .models import Category, Priority, Ticket, TicketNote, TicketStatus


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    ordering = ('level',)


@admin.register(TicketStatus)
class TicketStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order',)


class TicketNoteInline(admin.TabularInline):
    model = TicketNote
    extra = 0


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'requester', 'assigned_to', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'category')
    search_fields = ('code', 'title', 'description')
    inlines = [TicketNoteInline]

# Register your models here.
