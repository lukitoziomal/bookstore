from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegister


def register(response):
    if response.method == 'POST':
        form = UserRegister(response.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(response, user)
            return redirect('/')
    else:
        form = UserRegister()
    return render(response, 'registration/register.html', {'form': form})
