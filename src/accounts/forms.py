from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[(r.value, r.label) for r in User.Role if r != User.Role.COORDINATOR],
        widget=forms.Select(attrs={'class': 'form-select'})
     )
    class Meta:
        model = User
        fields = ('full_name', 'username', 'email', 'role')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirmar contraseña')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Usuario')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Contraseña')
