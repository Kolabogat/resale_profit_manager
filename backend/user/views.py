from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginFrom, SetUserPasswordForm


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
def account_profile(request):
    return render(request, 'user/account_profile.html')


@login_required
def user_data(request):
    return render(request, 'user/user_data.html')
