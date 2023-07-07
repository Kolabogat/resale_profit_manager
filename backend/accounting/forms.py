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
        fields = ['title', 'bought', 'sold']
