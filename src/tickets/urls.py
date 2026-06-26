from django.urls import path

from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.ticket_list, name='list'),
    path('create/', views.ticket_create, name='create'),
    path('<int:pk>/', views.ticket_detail, name='detail'),
    path('<int:pk>/edit/', views.ticket_update, name='update'),
    path('<int:pk>/delete/', views.ticket_delete, name='delete'),
    path('<int:pk>/notes/', views.ticket_add_note, name='add-note'),
    path('<int:pk>/close/', views.ticket_close, name='close'),
]
