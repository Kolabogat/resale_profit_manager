from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth import get_user_model


class UserLoginFrom(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


class SetUserPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ('new_password1', 'new_password2')
