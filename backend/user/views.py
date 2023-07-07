from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginFrom, SetUserPasswordForm
from django.db.models import Q
from accounting.models import Ticket
from django.db.models import Sum, Max, Min

from .models import UserAdditional


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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
def update_user_data(request):
    q = Q(user=request.user) & Q(deleted=False)
    tickets = Ticket.objects.filter(q)

    if UserAdditional.objects.filter(user=request.user):
        user_object = get_object_or_404(UserAdditional, user=request.user)
    else:
        user_object = UserAdditional()
        user_object.user = request.user

    user_object.all_time_profit = round(tickets.aggregate(Sum('profit')).get('profit__sum'), 2)
    user_object.tickets_quantity = tickets.count()
    user_object.highest_profit = round(tickets.aggregate(Max('profit')).get('profit__max'), 2)
    user_object.highest_loss = round(tickets.aggregate(Min('profit')).get('profit__min'), 2)
    user_object.save()

    user_object = get_object_or_404(UserAdditional, user=request.user)
    context = {
        'user_object': user_object,
    }
    return render(request, 'user/account_profile.html', context)



