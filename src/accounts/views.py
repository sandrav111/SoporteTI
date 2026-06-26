from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from .forms import UserLoginForm, UserRegistrationForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    form = UserLoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, 'Has iniciado sesión correctamente.')
        return redirect('core:dashboard')
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        messages.success(request, f'Usuario {user.username} creado correctamente.')
        return redirect('accounts:login')
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'La sesión ha finalizado.')
    return redirect('accounts:login')
