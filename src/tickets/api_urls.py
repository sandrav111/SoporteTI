from django.urls import path

from .api_views import (
    CategoryListAPIView,
    PriorityListAPIView,
    TicketListCreateAPIView,
    TicketNoteCreateAPIView,
    TicketRetrieveUpdateAPIView,
    TicketStatusListAPIView,
    TicketStatusUpdateAPIView,
)

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='api-categories'),
    path('priorities/', PriorityListAPIView.as_view(), name='api-priorities'),
    path('statuses/', TicketStatusListAPIView.as_view(), name='api-statuses'),
    path('tickets/', TicketListCreateAPIView.as_view(), name='api-ticket-list'),
    path('tickets/<int:pk>/', TicketRetrieveUpdateAPIView.as_view(), name='api-ticket-detail'),
    path('tickets/<int:pk>/status/', TicketStatusUpdateAPIView.as_view(), name='api-ticket-status'),
    path('tickets/<int:pk>/notes/', TicketNoteCreateAPIView.as_view(), name='api-ticket-notes'),
]
