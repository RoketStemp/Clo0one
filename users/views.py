from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .user_services import \
    select_current_user_and_user_info, \
    create_new_user_and_custom_user, \
    edit_current_user_personal_data, \
    add_subscriber_and_subscription_to_user, \
    get_all_users

from .forms import LoginForm, RegistrationForm, UserProfileEditForm


def user_login_view(request):
    """Log in user if can`t show errors otherwise redirect to the profile page"""
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
    """Create new user if password and confirm_password are the same and login was not used before,
    login him and redirect to the profile page"""
    if request.method == 'GET':
        form = RegistrationForm()
    else:
        form = RegistrationForm(request.POST)

        if request.POST['password'] != request.POST['confirm_password']:
            form.add_error('username', 'Password and Confirm password are different')

        if form.is_valid():
            user = create_new_user_and_custom_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return redirect('user_home_page_view', username=user.username)

    return render(request, 'users/registration.html', {
        'form': form
    })


def user_home_page_view(request, username):
    """Getting user info to show it on the user profile page selected by username"""
    user, user_info = select_current_user_and_user_info(username)

    return render(request, 'users/profile.html', {
        'user': user,
        'user_info': user_info
    })


def user_profile_edit_view(request, username):
    """Edit user personal data gotten from UserProfileEditForm
    and set previous values as initial to form"""
    user, user_info = select_current_user_and_user_info(username)
    print(user.first_name, user_info)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST)
        edit_current_user_personal_data(request=request, username=username)

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


def show_all_users_view(request):
    """Show all users"""
    users = get_all_users()
    return render(request, 'users/users.html', {
        'users': users
    })


def subscribe_view(request, username):
    add_subscriber_and_subscription_to_user(request, username)

    return redirect('show_all_users_view')
