from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginFrom, SetUserPasswordForm, UserSettingsForm
from django.db.models import Q
from accounting.models import Ticket
from django.db.models import Sum, Max, Min
from .models import UserProfile, UserSettings, CommandPagination, CommandCurrency


def user_additional_models(request):
    """
    Creates additional user models ('UserSettings' and
    'UserProfile') for individual user settings and data.
    """
    settings_user = UserSettings.objects.filter(user=request.user).exists()
    profile_user = UserProfile.objects.filter(user=request.user).exists()
    if not settings_user:
        settings_user = UserSettings()
        settings_user.user = request.user
        settings_user.save()

    if not profile_user:
        profile_user = UserProfile()
        profile_user.user = request.user
        profile_user.save()
    return


def register(request):
    """
    Shows 'register' template with 'UserRegisterForm' from
    that allow user to register.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            user_additional_models(request)

            messages.success(request, 'You successfully registered!')
            return redirect('home')
        else:
            messages.error(request, 'Registration error.')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


def user_login(request):
    """
    Shows 'login' template with 'UserLoginFrom' form
    that allow user to login.
    """
    if request.method == 'POST':
        form = UserLoginFrom(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            user_additional_models(request)

            messages.success(request, f'Welcome back {str(request.user.username).title()}. You successfully logged in!')
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UserLoginFrom()
    return render(request, 'user/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def password_change(request):
    """
    Shows 'password_change' template with 'SetUserPasswordForm' form
    that allow to update user password.
    """
    user = request.user
    if request.method == 'POST':
        form = SetUserPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been successfully changed.')
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetUserPasswordForm(user)
    return render(request, 'user/password_change.html', {'form': form})


@login_required
def view_user_data(request):
    """
    Shows 'account_profile' template with a user data: profit for
    all time, tickets quantity, highest profit, highest loss.
    """
    settings_user = UserSettings.objects.filter(user=request.user).get()
    user_object = get_object_or_404(UserProfile, user=request.user)

    context = {
        'user_object': user_object,
        'settings_user': settings_user,
        'title': 'User profile'
    }
    return render(request, 'user/account_profile.html', context)


@login_required
def update_user_data(request):
    """
    Updates 'UserProfile' data: profit for all time, tickets quantity,
    highest profit, highest loss.
    """
    try:
        q = Q(user=request.user) & Q(deleted=False)
        tickets = Ticket.objects.filter(q)
        user_object = get_object_or_404(UserProfile, user=request.user)

        if tickets:
            user_object.all_time_profit = round(tickets.aggregate(Sum('profit')).get('profit__sum'), 2)
            user_object.tickets_quantity = tickets.count()
            highest_profit = round(tickets.aggregate(Max('profit')).get('profit__max'), 2)
            if highest_profit >= 0:
                user_object.highest_profit = highest_profit
            highest_loss = round(tickets.aggregate(Min('profit')).get('profit__min'), 2)
            if highest_loss <= 0:
                user_object.highest_loss = highest_loss
            user_object.save()
            messages.success(request, 'You successfully updated your data.')
    except Exception:
        messages.error(request, 'You don\'t have any tickets.')
    return redirect('account_profile')


@login_required
def user_settings(request):
    """
    Shows 'user_settings' template with 'UserSettingsForm' form.
    User can change value that is used for pagination and
    currency symbol.
    Allow or disallow displaying currency symbol and ticket
    deletion confirmation.
    """
    settings_user = get_object_or_404(UserSettings, user=request.user)

    form = UserSettingsForm(instance=settings_user)

    command_pagination = CommandPagination.objects.filter().only('paginate_by')
    command_currency = CommandCurrency.objects.all()

    if request.method == 'POST':
        form = UserSettingsForm(request.POST or None, instance=settings_user)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            messages.success(request, 'Your settings saved.')
            return redirect('user_settings')

    context = {
        'form': form,
        'command_pagination': command_pagination,
        'command_currency': command_currency,
        'title': 'User settings',
    }
    return render(request, 'user/user_settings.html', context)
