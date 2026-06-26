from rest_framework import serializers

from .models import Category, Priority, Ticket, TicketNote, TicketStatus
from .services import add_note_to_ticket, create_ticket_from_data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ('id', 'name', 'level')


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = ('id', 'name', 'order')


class TicketSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(source='requester.full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.full_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    priority_name = serializers.CharField(source='priority.name', read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)

    class Meta:
        model = Ticket
        fields = (
            'id',
            'code',
            'title',
            'description',
            'category',
            'category_name',
            'priority',
            'priority_name',
            'status',
            'status_name',
            'requester',
            'requester_name',
            'assigned_to',
            'assigned_to_name',
            'feedback',
            'created_at',
            'updated_at',
            'closed_at',
        )
        read_only_fields = ('code', 'requester', 'created_at', 'updated_at', 'closed_at')
        extra_kwargs = {
            'assigned_to': {'required': False, 'allow_null': True},
            'status': {'required': False},
            'feedback': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        return create_ticket_from_data(validated_data, self.context['request'].user)

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.role == 'solicitante':
            for restricted_field in ('assigned_to', 'status', 'feedback'):
                validated_data.pop(restricted_field, None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance


class TicketStatusUpdateSerializer(serializers.Serializer):
    status = serializers.PrimaryKeyRelatedField(queryset=TicketStatus.objects.all())
    feedback = serializers.CharField(required=False, allow_blank=True)


class TicketNoteSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.full_name', read_only=True)

    class Meta:
        model = TicketNote
        fields = ('id', 'ticket', 'author', 'author_name', 'content', 'created_at')
        read_only_fields = ('ticket', 'author', 'created_at')

    def create(self, validated_data):
        return add_note_to_ticket(
            ticket=self.context['ticket'],
            author=self.context['request'].user,
            content=validated_data['content'],
        )
