from django.shortcuts import render

from .forms import LoginForm


def login(request):
    form = LoginForm()
    return render(request, 'users/login.html', {'form': form})
