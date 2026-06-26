from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import User

from .models import Category, Priority, Ticket, TicketStatus
from .serializers import (
    CategorySerializer,
    PrioritySerializer,
    TicketNoteSerializer,
    TicketSerializer,
    TicketStatusSerializer,
    TicketStatusUpdateSerializer,
)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class PriorityListAPIView(generics.ListAPIView):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer


class TicketStatusListAPIView(generics.ListAPIView):
    queryset = TicketStatus.objects.all()
    serializer_class = TicketStatusSerializer


class TicketListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = Ticket.objects.select_related('requester', 'assigned_to', 'category', 'priority', 'status')
        if self.request.user.role == 'solicitante':
            queryset = queryset.filter(requester=self.request.user)
        if status_id := self.request.query_params.get('status'):
            queryset = queryset.filter(status_id=status_id)
        return queryset


class TicketRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        queryset = Ticket.objects.select_related('requester', 'assigned_to', 'category', 'priority', 'status')
        if self.request.user.role == 'solicitante':
            queryset = queryset.filter(requester=self.request.user)
        return queryset


class TicketStatusUpdateAPIView(APIView):
    def patch(self, request, pk):
        if request.user.role not in {User.Role.TECHNICAL, User.Role.COORDINATOR, User.Role.ADMINISTRATOR}:
            return Response({'detail': 'No tienes permiso para cambiar el estado.'}, status=status.HTTP_403_FORBIDDEN)

        ticket = generics.get_object_or_404(Ticket.objects.visible_for_user(request.user), pk=pk)
        serializer = TicketStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket.status = serializer.validated_data['status']
        ticket.feedback = serializer.validated_data.get('feedback', ticket.feedback)
        ticket.save()
        return Response(TicketSerializer(ticket, context={'request': request}).data)


class TicketNoteCreateAPIView(APIView):
    def post(self, request, pk):
        ticket = generics.get_object_or_404(Ticket.objects.visible_for_user(request.user), pk=pk)
        serializer = TicketNoteSerializer(data=request.data, context={'request': request, 'ticket': ticket})
        serializer.is_valid(raise_exception=True)
        note = serializer.save()
        return Response(TicketNoteSerializer(note).data, status=status.HTTP_201_CREATED)
