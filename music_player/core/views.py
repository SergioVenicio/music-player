"""
    Views básicas do projeto, music-player
"""

from . import forms
from music_player import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .utils import get_all_musics, get_albuns, get_generos, get_bandas


def sign_up(request):
    if request.method == 'POST':
        form = forms.UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            usuario = authenticate(email=email, password=password)
            login(request, usuario)
            return redirect('home')
    else:
        form = forms.UsuarioForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


@login_required(login_url='/login')
def home(request):
    """ Retorna todos os albuns cadastrados no sistema """

    page = request.GET.get('page', 1)
    if not page:
        page = 1

    per_page = request.GET.get('per_page', None)
    if per_page is None or per_page == '':
        per_page = settings.PERPAGE
    generos = get_generos(per_page=per_page, page=page, pagination=True)

    context = {
        'generos': generos,
        'page': generos.number,
        'per_page': per_page,
        'total_pages': generos.paginator.num_pages
    }
    return render(request, 'core/home.html', context)


@login_required(login_url='/login')
def bandas(request, genero_id):
    page = request.GET.get('page', 1)
    if not page:
        page = 1

    per_page = request.GET.get('per_page', None)
    if per_page is None or per_page == '':
        per_page = settings.PERPAGE

    bandas = get_bandas(
        genero_id=genero_id, per_page=per_page, page=page, pagination=True
    )

    context = {
        'bandas': bandas,
        'page': bandas.number,
        'per_page': per_page,
        'total_pages': bandas.paginator.num_pages
    }
    return render(request, 'core/bandas.html', context)


@login_required(login_url='/login')
def albuns(request, banda_id):
    page = request.GET.get('page', 1)
    if not page:
        page = 1

    per_page = request.GET.get('per_page', None)
    if per_page is None or per_page == '':
        per_page = settings.PERPAGE

    albuns = get_albuns(
        banda_id=banda_id, per_page=per_page, page=page, pagination=True
    )

    context = {
        'albuns': albuns,
        'page': albuns.number,
        'per_page': per_page,
        'total_pages': albuns.paginator.num_pages
    }
    return render(request, 'core/albuns.html', context)


@login_required(login_url='/login')
def musicas(request, album_id):
    """ Retorna as músicas cadastradas no sistema com base no album """
    context = {
        'musics': get_all_musics(album_id=album_id),
        'album': get_albuns(album_id=album_id)
    }
    return render(request, 'core/musicas.html', context)


@login_required(login_url='/login')
def add_musicas(request):
    """ Adiciona musicas no banco de dados """
    if request.method == 'GET':
        form = forms.MusicaForm()
        context = {
            'form': form
        }
        return render(request, 'core/add_music.html', context=context)
    else:
        raise PermissionDenied()
