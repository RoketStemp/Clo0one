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
            return redirect('user_home_page_view', username=request.user.username)
        else:
            form.add_error('username', 'Username or password is incorrect')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {
        'form': form
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
            return redirect('user_home_page_view', username=user.username)

    return render(request, 'users/registration.html', {
        'form': form
    })


def user_home_page_view(request, username):
    """Getting user info to show it on the profile page got by username"""
    user = User.objects.get(username=username)
    user_info = CustomUser.objects.get(user=user.id)
    return render(request, 'users/profile.html', {
        'user': user,
        'user_info': user_info
    })


def user_profile_edit_view(request, username):
    """User profile edit view"""
    user = User.objects.get(username=username)
    user_info = CustomUser.objects.get(user=request.user.id)
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST)

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.username = request.POST['username']
        user.email = request.POST['email']
        if request.POST['profile_photo'] != '':
            user_info.profile_photo = request.POST['profile_photo']
        user_info.description = request.POST['description']
        user.save()
        user_info.save()
        return redirect('user_profile_edit_view', username=user.username)
    else:
        form = UserProfileEditForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
            'profile_photo': user_info.profile_photo,
            'description': user_info.description
        })
    return render(request, 'users/profile_edit.html', {
        'user': user,
        'user_info': user_info,
        'form': form
    })
