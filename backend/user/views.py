from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginFrom, SetUserPasswordForm, UserSettingsForm
from django.db.models import Q
from accounting.models import Ticket
from django.db.models import Sum, Max, Min
from .models import UserProfile, UserSettings, CommandPagination, CommandCurrency


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            settings_user = UserSettings()
            settings_user.user = request.user
            settings_user.save()

            profile_user = UserProfile()
            profile_user.user = request.user
            profile_user.save()

            messages.success(request, 'You successfully registered')
            return redirect('home')
        else:
            messages.error(request, 'Registration error')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginFrom(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginFrom()
    return render(request, 'user/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetUserPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been successfully changed')
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetUserPasswordForm(user)
    return render(request, 'user/password_change.html', {'form': form})


@login_required
def view_user_data(request):
    user_profile = UserProfile.objects.filter(user=request.user).get()
    user_settings = UserSettings.objects.filter(user=request.user).get()
    user_object = get_object_or_404(UserProfile, user=request.user)

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_settings': user_settings,
        'title': 'User profile'
    }
    return render(request, 'user/account_profile.html', context)


@login_required
def update_user_data(request):
    q = Q(user=request.user) & Q(deleted=False)
    tickets = Ticket.objects.filter(q)
    user_object = get_object_or_404(UserProfile, user=request.user)

    if tickets:
        user_object.all_time_profit = round(tickets.aggregate(Sum('profit')).get('profit__sum'), 2)
        user_object.tickets_quantity = tickets.count()
        user_object.highest_profit = round(tickets.aggregate(Max('profit')).get('profit__max'), 2)
        user_object.highest_loss = round(tickets.aggregate(Min('profit')).get('profit__min'), 2)
        user_object.save()
    return redirect('account_profile')


@login_required
def user_settings(request):
    settings_user = get_object_or_404(UserSettings, user=request.user)

    form = UserSettingsForm(instance=settings_user)

    command_pagination = CommandPagination.objects.filter().only('paginate_by')
    command_currency = CommandCurrency.objects.all()

    if request.method == 'POST':
        form = UserSettingsForm(request.POST or None, instance=settings_user)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            return redirect('user_settings')

    context = {
        'form': form,
        'command_pagination': command_pagination,
        'command_currency': command_currency,
        'title': 'User settings',
    }
    return render(request, 'user/user_settings.html', context)


