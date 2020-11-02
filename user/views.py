from django.shortcuts import render
from music_player import settings
from django.shortcuts import render, redirect
from django.views.decorators.http import etag
from django.contrib.auth import login, authenticate
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from . import forms


def sign_up(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            usuario = authenticate(email=email, password=password)
            login(request, usuario)
            return redirect('home')
    else:
        form = forms.UserForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


@login_required(login_url='/login')
def user_avatar(request):
    usuario = request.user
    if request.method == 'GET':
        form = forms.UserEditAvatar(instance=usuario)
    else:
        form = forms.UserEditAvatar(
            request.POST, request.FILES, instance=usuario
        )
        if form.is_valid():
            form.save()

    context = {
        'form': form,
        'avatar': usuario.avatar
    }
    return render(request, 'registration/avatar.html', context)
