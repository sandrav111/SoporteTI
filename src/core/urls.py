from django.urls import path

from .views import dashboard_view, home_redirect

app_name = 'core'

urlpatterns = [
    path('', home_redirect, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
