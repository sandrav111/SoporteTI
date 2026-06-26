from django import forms

from accounts.models import User

from .models import Ticket, TicketNote


SUPPORT_ROLES = {
    User.Role.TECHNICAL,
    User.Role.COORDINATOR,
    User.Role.ADMINISTRATOR,
}


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'category', 'priority')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
        }


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('title', 'description', 'category', 'priority', 'assigned_to', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(role__in=SUPPORT_ROLES)
        if not user or user.role not in SUPPORT_ROLES:
            self.fields.pop('assigned_to')
            self.fields.pop('status')


class TicketNoteForm(forms.ModelForm):
    class Meta:
        model = TicketNote
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
