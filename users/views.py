from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import LoginForm, RegistrationForm, UserProfileEditForm
from .models import User, CustomUser


def user_login_view(request):
    """Log in user if cant redirect to login page again"""
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

    return render(request, 'users/login.html', {
        'form': form
    })


def user_home_page_view(request):
    """Getting user info to show it on the profile page"""

    user_info = CustomUser.objects.get(user=request.user.id)
    return render(request, 'users/profile.html', {
        'user_info': user_info
    })


def user_logout_view(request):
    """Logout user"""
    logout(request)
    return redirect('user_login_view')


def user_registration_view(request):
    """Register user if password and confirm_password arent similar and login is unique"""
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

    return render(request, 'users/registration.html', {
        'form': form
    })


def user_profile_edit_view(request):
    """User profile edit view"""
    user_info = CustomUser.objects.get(user=request.user.id)
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST)
        u = User.objects.get(id=request.user.id)

        u.first_name = request.POST['first_name']
        u.last_name = request.POST['last_name']
        u.username = request.POST['username']
        u.email = request.POST['email']
        if request.POST['profile_photo'] != '':
            user_info.profile_photo = request.POST['profile_photo']
        user_info.description = request.POST['description']
        u.save()
        user_info.save()
        return redirect('user_profile_edit_view')
    else:
        form = UserProfileEditForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'username': request.user.username,
            'email': request.user.email,
            'profile_photo': user_info.profile_photo,
            'description': user_info.description
        })
    return render(request, 'users/profile_edit.html', {
        'user_info': user_info,
        'form': form
    })
