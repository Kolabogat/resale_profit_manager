from .models import Ticket
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import (
    CharField,
    TextInput,
    PasswordInput,
    ModelForm,
    Form,
    ImageField,
    inlineformset_factory,
)


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = ['user', 'closed', 'profit', 'category', 'created_at', 'closed_at']
        fields = "__all__"
