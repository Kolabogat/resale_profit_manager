from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.forms import ModelForm

from .models import UserSettings


class UserLoginFrom(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


class SetUserPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ('new_password1', 'new_password2')


class UserSettingsForm(ModelForm):
    class Meta:
        model = UserSettings
        fields = ('paginate_by', 'currency', 'display_symbol', 'delete_confirmation')
