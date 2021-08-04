from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import LoginForm, RegistrationForm
from .models import User


def user_login_view(request):
    """View which allows user to log in on site"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('user_home_page_view')
        else:
            form.add_error('username', 'Username or password is incorrect')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def user_home_page_view(request):
    """User for showing current user data got by slug"""
    return render(request, 'users/profile.html')


def user_logout_view(request):
    """User logout view"""
    logout(request)
    return redirect('user_login_view')


def user_registration_view(request):
    """User registration view"""
    if request.method == 'GET':
        form = RegistrationForm()
    else:
        form = RegistrationForm(request.POST)

        if request.POST['password'] != request.POST['confirm_password']:
            form.add_error('username', 'Password and Confirm password are different')

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('user_home_page_view')

    return render(request, 'users/registration.html', {'form': form})
