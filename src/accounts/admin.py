from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'full_name', 'email', 'role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Informacion adicional', {'fields': ('full_name', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informacion adicional', {'fields': ('full_name', 'email', 'role')}),
    )

# Register your models here.
